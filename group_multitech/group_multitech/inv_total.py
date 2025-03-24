import frappe

@frappe.whitelist()
def get_totals():
	contracts = frappe.get_all("Contract", fields=["name"])
	for c in contracts:
		totals = frappe.get_all("Sales Invoice", fields=["sum(total) as total", "sum(net_total) as net_total"], filters={"customer_contract": c.name, "docstatus": ("!=", 2)})
		if totals:
			total = totals[0].total or 0
			net_total = totals[0].net_total or 0
			if not total:
				total = 0
			if not net_total:
				net_total = 0
			frappe.db.set_value("Contract", c.name, "total_amount_with_tax", total)
			frappe.db.set_value("Contract", c.name, "net_amount", net_total)
		else:
			frappe.db.set_value("Contract", c.name, "total_amount_with_tax", 0)
			frappe.db.set_value("Contract", c.name, "net_amount", 0)