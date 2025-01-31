from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
	if not filters:
		filters = {}
	data  = []
	columns = get_column()
	conditions = get_conditions(filters)
	master = get_master(conditions, filters)


	for m in master:
		row = {}
		row["invoice_date"] = m.posting_date;
		row["invoice_name"] = m.name;
		row["customer"] = m.customer;
		row["project"] = m.project;
		row["sales_net_total"] = m.net_total;
		row["sales_amount"] = m.total_taxes_and_charges;
		row["sales_tax_total"] = m.total_taxes_and_charges;
		row["commercial_invoice_date"] = m.commercial_invoice_date;
		row["sales_tax_invoice_date"] = m.sales_tax_invoice_date;

		payment_cond = get_conditions_for_payments(filters)
		payment_data = get_payment_data(m.name,payment_cond)
		# frappe.msgprint(str(payment_data))
		for d in payment_data:
			row["payment_date"] = d.get("posting_date")
			row["payment_name"] = d.get("name")
			row["reference_no"] = d.get("reference_name")
			row["reference_date"] = d.get("due_date")
			row["allocated_amount"] = d.get("allocated_amount")
			row["paid_amount"] = d.get("paid_amount")
			deduction = frappe.db.sql("select SUM(amount) from `tabPayment Entry Deduction` where parent = '{}'".format(d.get("name")))
			if deduction and len(deduction):
				row["deduction"] = deduction[0][0]
		data.append(row)

	return columns, data



def get_column():
	return [

		{
			"fieldname":"invoice_date",
			"label": "Invoice Date",
			"width": 90,
			"fieldtype": "Date",

		},
		{
			"fieldname": "invoice_name",
			"label": ("Sales Invoice"),
			"fieldtype": "Link",
			"width": 150,
			"options": "Sales Invoice",
		},


		{
			"fieldname": "customer",
			"label": ("Customer"),
			"fieldtype": "Link",
			"width": 150,
			"options": "Customer",
		},


		{
			"fieldname": "project",
			"label": ("Project"),
			"fieldtype": "Link",
			"width": 150,
			"options": "Project",
		},


		{
			"fieldname":"sales_net_total",
			"label": "Net Total",
			"width": 150,
			"fieldtype": "Currency",
		},


		{
			"fieldname": "sales_amount",
			"label": ("Amount"),
			"fieldtype": "Currency",
			"width": 80,
		},

		{
			"fieldname": "sales_tax_total",
			"label": ("Sales Tax Total"),
			"fieldtype": "Currency",
			"width": 150,
		},



		{
			"fieldname": "commercial_invoice_date",
			"label": ("Commercial Invoice Date "),
			"fieldtype": "Date",
			"width": 170,
		},


		{
			"fieldname": "sales_tax_invoice_date",
			"label": ("Sales Tax Invoice Date "),
			"fieldtype": "Date",
			"width": 150,
		},


		{
			"fieldname":"payment_date",
			"label": "Payment Date",
			"width": 110,
			"fieldtype": "Date",

		},
		{
			"fieldname": "payment_name",
			"label": ("Payment Entry"),
			"fieldtype": "Link",
			"width": 150,
			"options": "Payment Entry",
		},

		{
			"fieldname":"reference_no",
			"label": "Reference No",
			"width": 150,
			"fieldtype": "Data",
		},


		{
			"fieldname":"reference_date",
			"label": ("Reference Date"),
			"fieldtype": "Date",
			"width": 150,
		},

		{
			"fieldname": "allocated_amount",
			"label": ("Allocated Amount"),
			"fieldtype": "Currency",
			"width": 150,
		},



		{
			"fieldname": "paid_amount",
			"label": ("Paid Amount "),
			"fieldtype": "Currency",
			"width": 150,
		},


		{
			"fieldname": "deduction",
			"label": ("Deduction "),
			"fieldtype": "Currency",
			"width": 150,
		},

	]

	
	
	return columns



def get_master(conditions,filters):
	data = frappe.db.sql(""" select si.posting_date , si.name ,  si.customer , si.project ,   si.net_total , si.total_taxes_and_charges, si.total_taxes_and_charges,
		si.commercial_invoice_date , si.sales_tax_invoice_date
		from `tabSales Invoice` si  where si.docstatus = 1  and si.outstanding_amount < si.rounded_total  %s  order by si.name desc   """%(conditions), filters, as_dict=1)
	return data


# def get_data(Sale_invoice = None , payment_date_1 = None, payment_date_2 = None ,  ):
# 	data = frappe.db.sql(""" select  pe.posting_date ,  pe.name , per.reference_name , per.due_date , per.allocated_amount 
# 		from `tabPayment Entry` pe  inner join `tabPayment Entry Reference` per
# 		on pe.name = per.parent  where pe.docstatus = 1 and per.reference_name  = {}  %s  order by pe.name  desc   """%(conditions), filters, as_list=1)
# 	return data




def get_payment_data(sales_invoice, payment_cond=None):
	data = frappe.db.sql("""
		select  pe.posting_date as posting_date , pe.paid_amount as paid_amount,  pe.name as name, per.reference_name as reference_name , per.due_date  as due_date, per.allocated_amount as allocated_amount
		from `tabPayment Entry` pe  inner join `tabPayment Entry Reference` per
		on pe.name = per.parent  where pe.docstatus = 1 and per.reference_name  = '{}' {} """.format(sales_invoice, payment_cond), as_dict=1)
	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("company"):
		conditions += " and si.company =  %(company)s"

	if filters.get("invoice_from_date") and  filters.get("sales_tax_invoice_from_date"):
		conditions += " and (si.commercial_invoice_date <= '{}' or si.sales_tax_invoice_date <= '{}')".format(filters.get("invoice_from_date"), filters.get("sales_tax_invoice_from_date"))
	else:
		if filters.get("invoice_from_date"):
			conditions += " and si.commercial_invoice_date <= '{}'".format(filters.get("invoice_from_date"))

		if filters.get("sales_tax_invoice_from_date"):
			conditions += " and si.sales_tax_invoice_date <=  '{}'".format(filters.get("sales_tax_invoice_from_date"))

	return conditions


def get_conditions_for_payments(filters):
	conditions = ""

	if filters.get("invoice_from_date") and  filters.get("sales_tax_invoice_from_date"):
		conditions += " and (pe.posting_date >=  '{}' or pe.posting_date >=  '{}')".format(filters.get("invoice_from_date"), filters.get("sales_tax_invoice_from_date"))
	else:
		if filters.get("invoice_from_date"):
			conditions += " and pe.posting_date >=  '{}'".format(filters.get("invoice_from_date"))

		if filters.get("sales_tax_invoice_from_date"):
			conditions += " and pe.posting_date >=  '{}'".format(filters.get("sales_tax_invoice_from_date"))

	return conditions