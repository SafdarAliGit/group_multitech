import frappe
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry


def validate_warehouse(self):
    frappe.throw('here')
    """perform various (sometimes conditional) validations on warehouse"""

    source_mandatory = ["Material Issue", "Material Transfer", "Send to Subcontractor", "Material Transfer for Manufacture",
        "Material Consumption for Manufacture", "Send to Warehouse", "Receive at Warehouse"]

    target_mandatory = ["Material Receipt", "Material Transfer", "Send to Subcontractor",
        "Material Transfer for Manufacture", "Send to Warehouse", "Receive at Warehouse"]

    validate_for_manufacture = any([d.bom_no for d in self.get("items")])

    if self.purpose in source_mandatory and self.purpose not in target_mandatory:
        self.to_warehouse = None
        for d in self.get('items'):
            d.t_warehouse = None
    elif self.purpose in target_mandatory and self.purpose not in source_mandatory:
        self.from_warehouse = None
        for d in self.get('items'):
            d.s_warehouse = None

    for d in self.get('items'):
        if not d.s_warehouse and not d.t_warehouse:
            d.s_warehouse = self.from_warehouse
            d.t_warehouse = self.to_warehouse

        if not (d.s_warehouse or d.t_warehouse):
            frappe.throw(_("Atleast one warehouse is mandatory"))

        if self.purpose in source_mandatory and not d.s_warehouse:
            if self.from_warehouse:
                d.s_warehouse = self.from_warehouse
            else:
                frappe.throw(_("Source warehouse is mandatory for row {0}").format(d.idx))

        if self.purpose in target_mandatory and not d.t_warehouse:
            if self.to_warehouse:
                d.t_warehouse = self.to_warehouse
            else:
                frappe.throw(_("Target warehouse is mandatory for row {0}").format(d.idx))

        if self.purpose == "Manufacture":
            if validate_for_manufacture:
                if d.bom_no:
                    d.s_warehouse = None
                    if not d.t_warehouse:
                        frappe.throw(_("Target warehouse is mandatory for row {0}").format(d.idx))
                else:
                    d.t_warehouse = None
                    if not d.s_warehouse:
                        frappe.throw(_("Source warehouse is mandatory for row {0}").format(d.idx))

        # if cstr(d.s_warehouse) == cstr(d.t_warehouse) and not self.purpose == "Material Transfer for Manufacture":
        #     frappe.throw(_("Source and target warehouse cannot be same for row {0}").format(d.idx))


def CustomStockEntry():
    StockEntry.validate_warehouse = validate_warehouse