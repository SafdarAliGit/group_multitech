# Copyright (c) 2013, Hardik Gadesha and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
from frappe import _
import frappe
from frappe.utils import flt, cint, cstr, date_diff

def execute(filters=None):
	if not filters:
		filters = {}

	project_conditions = get_project_conditions(filters)
	date_conditions = get_date_conditions(filters)
	columns = get_column()

	projects = get_projects(project_conditions, filters)
	project_totals = get_project_value2nd(project_conditions,date_conditions, filters) or get_project_value(project_conditions,date_conditions, filters)
	# latest_po_date = get_latest_po_date(project_conditions,date_conditions, filters)
	# latest_po_date = get_latest_po_date(project_conditions,date_conditions, filters)
	expense_claim_total = get_expense_claim_total(project_conditions,date_conditions, filters)
	received_payment_total = get_received_payment_total(project_conditions,date_conditions, filters)
	material_cost_total = get_material_cost_total(project_conditions,date_conditions, filters)
	service_cost_total = get_service_cost_total(project_conditions,date_conditions, filters)
	withholding_tax = get_withholding_tax(project_conditions,date_conditions, filters)
	sales_tax_gst = get_gst(project_conditions,date_conditions, filters)
	
	data = []

	float_precision = cint(frappe.db.get_default("float_precision")) or 3
	for p in projects:
		project_name = p.get("name")
		row = {}
		completion_date = ''
		total_sst = 0
		total_gst = 0
		row['project_name'] = project_name
		row["period_of_project"] = str(p.get("expected_start_date") or "")+" "+str(p.get("expected_end_date") or "")
		row['value_of_project'] = 0
		row['payment_recived'] = 0
		row['cost_of_material'] = 0
		row['cost_of_services'] = 0
		row['total_other_expense'] = 0
		row['pnl_amount'] = 0
		
		for i in project_totals:
			if i.get('project') == project_name:
				row['value_of_project'] = i.get('grand_total')

		# for i in latest_po_date:
		# 	if i.get('project') == project_name:
		# 		row['period_of_project'] = i.get('po_date')
		# 		completion_date = i.get('completion_date')
				
		if p.get('expected_end_date') and p.get("completion_date"):
			period_of_completion_or_late = date_diff(p.get("completion_date"), p.get('expected_end_date'))
			row['period_of_completion_or_late'] = period_of_completion_or_late
			
		for d in received_payment_total:
			if d.get('project') == project_name:
				row['payment_recived'] = d.get('total_recvd_payment')

		for d in withholding_tax:
			if d.get('project') == project_name:
				total_sst = abs(d.get('total_sst'))

		for d in sales_tax_gst:
			if d.get('project') == project_name:
				total_gst = abs(d.get('total_gst'))

		row['withholding_Tax'] = total_sst + total_gst

		for d in expense_claim_total:
			if d.get('project') == project_name:
				row['total_other_expense'] = d.get('total_expense')


		for d in material_cost_total:
			if d.get('project') == project_name:
				row['cost_of_material'] = d.get('total_material_cost')
			
		for d in service_cost_total:
			if d.get('project') == project_name:
				row['cost_of_services'] = d.get('total_service_cost')



		total_other_expense = flt(row.get('total_other_expense'), )
		cost_of_services = flt(row.get('cost_of_services'))
		cost_of_material = flt(row.get('cost_of_material'))
		payment_received = flt(row.get('payment_recived'))

		over_head_values = 0 if total_other_expense==0 else (cost_of_services / total_other_expense) * 100
		
		expenses = cost_of_material + cost_of_services + total_other_expense
		pnl = payment_received - expenses
		profit_loss_perc =  0 if payment_received==0 else (expenses / payment_received) * 100

		profit_loss_perc  = "-" + cstr(profit_loss_perc) if pnl<0 else profit_loss_perc
		row['overHead_value_wise'] = flt(over_head_values, float_precision)
		row['pnl_amount'] = flt(pnl)
		row['profit_loss_perc'] = flt(profit_loss_perc, float_precision)

		data.append(row)
	
	return columns, data

def get_projects(p_conditions, filters):
	data = frappe.db.sql("""select * from `tabProject` p where 1 = 1 %s """%(p_conditions), filters, as_dict=1)
	return data

def get_project_value(p_conditions, d_conditions, filters):
	data = frappe.db.sql("""select sum(si.rounded_total) as grand_total, si.project from `tabProject` p 
	inner join `tabSales Invoice` si on p.name = si.project
	where si.docstatus = 1  %s %s group by 2"""%(p_conditions,d_conditions), filters, as_dict=1)

	return data

def get_project_value2nd(p_conditions, d_conditions, filters):
	data = frappe.db.sql("""select sum(t.total) as grand_total, si.project from `tabProject` p 
	inner join `tabSales Invoice` si on p.name = si.project
	inner join `tabSales Taxes and Charges` t on p.name = t.parent
	where si.docstatus = 1 and t.idx = 1  %s %s group by 2"""%(p_conditions,d_conditions), filters, as_dict=1)

	return data

def get_latest_po_date(p_conditions, d_conditions, filters):
	data = frappe.db.sql("""select si.po_date, si.project, p.completion_date from `tabProject` p 
	inner join `tabSales Invoice` si on p.name = si.project
	where si.docstatus = 1 and si.po_date is not null %s %s group by 2 order by si.posting_date desc"""%(p_conditions,d_conditions), filters, as_dict=1)

	return data

def get_received_payment_total(p_conditions,d_conditions, filters):
	d_conditions = ""
	if filters.get("from_date"):
		filters.from_date = filters.get('from_date')
		d_conditions += " and si.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		filters.to_date = filters.get('to_date')
		d_conditions += " and si.posting_date <= %(to_date)s"

	data = frappe.db.sql("""select sum(pe.paid_amount) as total_recvd_payment, si.project from 
	 `tabPayment Entry` pe
	inner join `tabPayment Entry Reference` pr on pe.name = pr.parent
	inner join `tabSales Invoice` si on si.name = pr.reference_name
	inner join `tabProject` p on si.project = p.name
	where pe.docstatus = 1 and pe.project is not null  %s %s group by 2"""%(p_conditions,d_conditions), filters, as_dict=1)

	return data

def get_withholding_tax(p_conditions,d_conditions, filters):
	# account = frappe.db.escape('2304 - SST WHT 20% - ME')
	account = frappe.db.escape(filters.get("account_withholding"))
	data = frappe.db.sql("""select sum(st.tax_amount) as total_sst, si.project from `tabProject` p 
	inner join `tabSales Invoice` si on p.name = si.project
	inner join `tabSales Taxes and Charges` st on si.name = st.parent
	where si.docstatus = 1 and si.sales_tax != 'GST' and st.account_head like %s
	%s %s group by 2"""%(account, p_conditions,d_conditions), filters, as_dict=1)

	return data

def get_gst(p_conditions,d_conditions, filters):
	account = frappe.db.escape('2308 - Income Tax 4.5% on Supply - MES')
	data = frappe.db.sql("""select sum(ped.amount) as total_gst, pe.project from `tabProject` p 
	inner join `tabPayment Entry` pe on p.name = pe.project
	inner join `tabPayment Entry Deduction` ped on pe.name = ped.parent
	where pe.docstatus = 1 and pe.project is not null and ped.account like %s
	%s %s group by 2"""%(account, p_conditions,d_conditions), filters, as_dict=1)

	return data

def get_material_cost_total(p_conditions,d_conditions, filters):
	data = frappe.db.sql("""select sum(pii.net_amount) as total_material_cost, pii.project from `tabProject` p 
	inner join `tabPurchase Invoice Item` pii on pii.project = p.name
	inner join `tabPurchase Invoice` pi on pi.name = pii.parent 
	where pi.docstatus = 1 and pi.purchase_type = 'Supply' %s %s group by 2"""%(p_conditions,d_conditions), filters, as_dict=1)

	return data

def get_service_cost_total(p_conditions,d_conditions, filters):
	data = frappe.db.sql("""select sum(pii.net_amount) as total_service_cost, pii.project from `tabProject` p 
	inner join `tabPurchase Invoice Item` pii on pii.project = p.name
	inner join `tabPurchase Invoice` pi on pi.name = pii.parent 
	where pi.docstatus = 1 and pi.purchase_type = 'Services' %s %s group by 2"""%(p_conditions,d_conditions), filters, as_dict=1)

	return data

def get_expense_claim_total(p_conditions,d_conditions, filters):
	data = frappe.db.sql("""select sum(ec.total_amount_reimbursed) as total_expense, ec.project from `tabProject` p 
	inner join `tabExpense Claim` ec on p.name = ec.project
	where ec.docstatus = 1  %s %s group by 2"""%(p_conditions,d_conditions), filters, as_dict=1)

	return data


def get_project_conditions(filters):
	conditions = ""
	if filters.get("project"):
		filters.project = frappe.parse_json(filters.get('project'))
		conditions += " and p.name in %(project)s"
	if filters.get("cost_center"):
		filters.cost_center = frappe.parse_json(filters.get('cost_center'))
		conditions += " and p.cost_center in %(cost_center)s"

	if filters.get("company"):
		filters.company = filters.get('company')
		conditions += " and p.company = %(company)s"

	return conditions

def get_date_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		filters.from_date = filters.get('from_date')
		conditions += " and posting_date >= %(from_date)s"
	if filters.get("to_date"):
		filters.to_date = filters.get('to_date')
		conditions += " and posting_date <= %(to_date)s"
	return conditions

def get_column():
	columns = [{
			"fieldname": "project_name",
			"label": _("Project Name"),
			"fieldtype": "Link",
			"options": "Project",
			"width": 300
		},
		{
			"fieldname": "value_of_project",
			"label": _("Value Of Project "),
			"fieldtype": "Currency",
			"options": "",
			"width": 160
		},

		{
			"fieldname": "period_of_project",
			"label": _("Period Of project"),
			"fieldtype": "Data",
			"options": "",
			"width": 160
		},

		{
			"fieldname": "period_of_completion_or_late",
			"label": _("Period of Completion OR Late"),
			"fieldtype": "Data",
			"options": "",
			"width": 160
		},
		{
			"fieldname": "payment_recived",
			"label": _("Payment Recived"),
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"fieldname": "withholding_Tax",
			"label": _("withholding Tax"),
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"fieldname": "cost_of_material",
			"label": _("Cost OF Material "),
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"fieldname": "cost_of_services",
			"label": _("Cost OF Services"),
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"fieldname": "total_other_expense",
			"label": _("Total Other Expense"),
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"fieldname": "overHead_value_wise",
			"label": _("OverHead % value Wise"),
			"fieldtype": "Percent",
			"width": 160
		},
		{
			"fieldname": "pnl_amount",
			"label": _("PNL Amount"),
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"fieldname": "profit_loss_perc",
			"label": _("Amount of Profit/Loss in %"),
			"fieldtype": "Data",
			"width": 160
		},
	]

	return columns
