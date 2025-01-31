# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_column()
	conditions = get_conditions(filters)
	data = get_data(conditions, filters)

	return columns, data

def get_column():
	return [_("Cost Center") + ":Link/Cost Center:120", _("Project") + ":Link/Project:150", _("Project Status") + ":Data:120", 
		_("Customer") + ":Link/Customer:120", _("Sales Inv No") + ":Link/Sales Invoice:120", 
		_("Sales Inv Amount") + ":Currency:130", _("Sales Inv Status") + ":Data:120",
		_("SI Commercial Date") + ":Date:150", _("SI Sales Tax Date") + ":Date:150",
		_("Supplier") + ":Link/Supplier:120", _("Purchase Inv No") + ":Link/Purchase Invoice:130",
		_("Purchase Inv Amount") + ":Currency:140", _("Purchase Inv Status") + ":Data:130"
	]

def get_data(conditions, filters):
	data = frappe.db.sql("""select p.cost_center, p.name, p.status from `tabProject` p where p.name = 'ABC NISHAN-E-HAIDER CHOWK'
	 	%s order by p.name ASC
		"""%(conditions), filters, as_list=1)

	mylist = []

	for d in data:
		sales_inv = frappe.db.sql("""select s.customer, s.name, s.net_total, s.status,s.commercial_invoice_date, 
			s.sales_tax_invoice_date from `tabSales Invoice` s where s.project = '%s' and s.docstatus != 2 %s
			order by s.name DESC
			"""%(d[1],conditions), filters, as_list=1)
		mylist.append(d[0])
		mylist.append(d[1])
		mylist.append(d[2])
		if sales_inv:
			mylist + sales_inv
	return mylist

def get_conditions(filters):
	conditions = ""
	# if filters.get("from_date"):
	# 	conditions += " and `tabTimesheet`.start_date >= timestamp(%(from_date)s)"
	# if filters.get("to_date"):
	# 	conditions += " and `tabTimesheet`.start_date <= timestamp(%(to_date)s)"
	# if filters.get("emp_id"):
	# 	conditions += " and `tabTimesheet`.employee = %(emp_id)s"

	match_conditions = build_match_conditions("Project")
	if match_conditions:
		conditions += " and %s" % match_conditions

	return conditions

@frappe.whitelist()
def test():
	data = frappe.db.sql("""select p.cost_center, p.name, p.status from `tabProject` p where p.name = 'ABC NISHAN-E-HAIDER CHOWK' order by p.name ASC""",as_list=1)

	sales_inv = []

	for d in data:
		query = """select s.customer, s.name, s.net_total, s.status,s.commercial_invoice_date, 
			s.sales_tax_invoice_date from `tabSales Invoice` s where s.project = '{0}' and s.docstatus != 2
			order by s.name DESC
			""".format(d[1])
		sales_inv = frappe.db.sql(query,as_list=1)
	# print(sales_inv)
		if sales_inv:
			data+=sales_inv
	print(data)