import frappe

@frappe.whitelist()
def get_pi(doctype, txt, searchfield, start, page_len, filters):
	if filters.get("project") and filters.get("supplier"):
		return frappe.db.sql("""select p.name
				from `tabPurchase Invoice` p INNER JOIN `tabPurchase Invoice Item` c on p.name = c.parent
				where (p.supplier = %(supplier)s) and (p.name like %(txt)s) and (c.project = %(project)s)
				and (p.docstatus != 2)
				limit %(page_length)s""", {
					'txt': '%' + txt + '%',
					'supplier': filters.get("supplier"),
					'project': filters.get("project"),
					'page_length': page_len
				})
	elif not filters.get("project") and filters.get("supplier"):
		return frappe.db.sql("""select p.name
				from `tabPurchase Invoice` p 
				where (p.supplier = %(supplier)s) and (p.name like %(txt)s)
				and (p.docstatus != 2)
				limit %(page_length)s""", {
					'txt': '%' + txt + '%',
					'supplier': filters.get("supplier"),
					'page_length': page_len
				})
	elif not filters.get("project") and not filters.get("supplier"):
		return frappe.db.sql("""select p.name
				from `tabPurchase Invoice` p 
				where (p.name like %(txt)s)
				and (p.docstatus != 2)
				limit %(page_length)s""", {
					'txt': '%' + txt + '%',
					'page_length': page_len
				})

@frappe.whitelist()
def get_invoice_items(name):
	items = []
	item_names = []
	qty = []
	projects = []
	invoices = []
	uoms = []
	cost_centers = []
	expenses = []
	# pi = frappe.get_doc("Purchase Invoice", name)
	import json
	name = json.loads(name)
	if name:
		for i in name:
			invoice = frappe.get_doc("Sales Invoice", i["sales_invoice"])
			for d in invoice.get("items"):
				items.append(d.item_code)
				item_names.append(d.item_name)
				uoms.append(d.uom)
				cost_centers.append(d.cost_center)
				expenses.append(d.expense_account)
				qty.append(d.qty)
				projects.append(invoice.project)
				invoices.append(i["sales_invoice"])
	return {"items": items, "qty": qty, "projects":projects, "invoices": invoices, "item_names": item_names, "uoms": uoms, "cost_centers":cost_centers, "expenses": expenses}


@frappe.whitelist()
def check_taxes():
	accounts = []
	data = frappe.db.sql("select account from `tabTaxes Account` where parent = 'Taxes'")
	if data:
		for d in data:
			accounts.append(d[0])
	return accounts

# @frappe.whitelist()
# def get_invoice_items(name):
# 	items = []
# 	item_names = []
# 	qty = []
# 	projects = []
# 	invoices = []
# 	uoms = []
# 	cost_centers = []
# 	pi = frappe.get_doc("Purchase Invoice", name)
# 	if pi.sales_invoices:
# 		for i in pi.get("sales_invoices"):
# 			invoice = frappe.get_doc("Sales Invoice", i.sales_invoice)
# 			for d in invoice.get("items"):
# 				items.append(d.item_code)
# 				item_names.append(d.item_name)
# 				uoms.append(d.uom)
# 				cost_centers.append(d.cost_center)
# 				qty.append(d.qty)
# 				projects.append(invoice.project)
# 				invoices.append(i.sales_invoice)
# 	return {"items": items, "qty": qty, "projects":projects, "invoices": invoices, "item_names": item_names, "uoms": uoms, "cost_centers":cost_centers}