from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document
from frappe.utils import flt
import erpnext.controllers.taxes_and_totals

@frappe.whitelist(allow_guest=True)
def sales_tax_series(sales_tax,company):
	query= frappe.db.sql("SELECT MAX(tax_number) FROM  `tabSales Invoice` WHERE is_return = 0 and  sales_tax = '"+str(sales_tax)+"' and company = '"+str(company)+"';")
	return query

@frappe.whitelist(allow_guest=True)
def sales_tax_series2(sales_tax,company,name, tax_number):
	query = frappe.db.get_value("Sales Invoice", {"docstatus": ("!=", 2), "tax_number": tax_number, "sales_tax": sales_tax, "company": company, "name":("!=", name), "is_return": 0}, "name")
	# query= frappe.db.sql("SELECT name FROM  `tabSales Invoice` WHERE name != '"+str(name)+" and tax_number = '"+str(tax_number)+"' and sales_tax = '"+str(sales_tax)+"' and company = '"+str(company)+"' and docstatus != 2';")
	if query:
		return query

def test(doc,method):
	frappe.throw("There" + method + " : " + doc.name)