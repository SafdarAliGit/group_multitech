import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice as StockSalesInvoice

class SalesInvoice(StockSalesInvoice):
    @frappe.whitelist()
    def fetch_price_list(self):
        if frappe.db.exists("Contract", self.customer_contract):
            price_list = frappe.db.get_value("Contract", self.customer_contract, "custom_price_list")
            return price_list
        