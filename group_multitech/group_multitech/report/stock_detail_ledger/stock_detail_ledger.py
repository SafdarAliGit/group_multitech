# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.stock.utils import update_included_uom_in_report

def execute(filters=None):
	include_uom = filters.get("include_uom")
	columns = get_columns()
	items = get_items(filters)
	sl_entries = get_stock_ledger_entries(filters, items)
	item_details = get_item_details(items, sl_entries, include_uom)
	opening_row = get_opening_balance(filters, columns)

	data = []
	conversion_factors = []
	if opening_row:
		data.append(opening_row)

	actual_qty = stock_value = 0

	for sle in sl_entries:
		item_detail = item_details[sle.item_code]

		sle.update(item_detail)

		if filters.get("batch_no"):
			actual_qty += sle.actual_qty
			stock_value += sle.stock_value_difference

			if sle.voucher_type == 'Stock Reconciliation':
				actual_qty = sle.qty_after_transaction
				stock_value = sle.stock_value

			sle.update({
				"qty_after_transaction": actual_qty,
				"stock_value": stock_value
			})

		data.append(sle)

		if include_uom:
			conversion_factors.append(item_detail.conversion_factor)

	update_included_uom_in_report(columns, data, include_uom, conversion_factors)
	return columns, data

def get_columns():
	columns = [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Datetime", "width": 95},
		{"label": _("SAP Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 90},
		{"label": _("Item Name"), "fieldname": "item_name1", "width": 200},
		# {"label": _("Item Group"), "fieldname": "item_group", "fieldtype"/: "Link", "options": "Item Group", "width": 100},
		# {"label": _("Brand"), "fieldname": "brand", "fieldtype": "Link", "options": "Brand", "width": 100},
		# {"label": _("Description"), "fieldname": "description", "width": 200},
		# {"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 100},
		{"label": _("Unit"), "fieldname": "stock_uom", "fieldtype": "Link", "options": "UOM", "width": 60},
		{"label": _("Qty"), "fieldname": "actual_qty", "fieldtype": "Float", "width": 100, "convertible": "qty"},
		{"label": _("Balance Qty"), "fieldname": "qty_after_transaction", "fieldtype": "Float", "width": 100, "convertible": "qty"},
		# {"label": _("Incoming Rate"), "fieldname": "incoming_rate", "fieldtype": "Currency", "width": 110,
		# 	"options": "Company:company:default_currency", "convertible": "rate"},
		# {"label": _("Valuation Rate"), "fieldname": "valuation_rate", "fieldtype": "Currency", "width": 110,
		# 	"options": "Company:company:default_currency", "convertible": "rate"},
		# {"label": _("Balance Value"), "fieldname": "stock_value", "fieldtype": "Currency", "width": 110,
		# 	"options": "Company:company:default_currency"},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "width": 110},
		{"label": _("Voucher #"), "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 100},
		# {"label": _("Batch"), "fieldname": "batch_no", "fieldtype": "Link", "options": "Batch", "width": 100},
		# {"label": _("Serial #"), "fieldname": "serial_no", "width": 100},
		{"label": _("Team"), "fieldname": "team", "fieldtype": "Link", "options": "Team", "width": 100},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 100},
		{"label": _("PMT"), "fieldname": "pmt", "fieldtype": "Link", "options": "PMT", "width": 100},
		{"label": _("KE Store"), "fieldname": "ke_store", "fieldtype": "Link", "options": "KE Store", "width": 100},
		{"label": _("STO"), "fieldname": "sto", "fieldtype": "Link", "options": "STO", "width": 100},
		{"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 110}
	]

	return columns

def get_stock_ledger_entries(filters, items):
	item_conditions_sql = ''
	if items:
		item_conditions_sql = 'and sle.item_code in ({})'\
			.format(', '.join([frappe.db.escape(i) for i in items]))

	return frappe.db.sql("""select concat_ws(" ", posting_date, posting_time) as date,
			team,pmt,ke_store,sto,
			item_code, warehouse, actual_qty, qty_after_transaction, incoming_rate, valuation_rate,
			stock_value, voucher_type, voucher_no, batch_no, serial_no, company, project, stock_value_difference
		from `tabStock Ledger Entry` sle
		where company = %(company)s and
			posting_date between %(from_date)s and %(to_date)s
			{sle_conditions}
			{item_conditions_sql}
			order by posting_date asc, posting_time asc, creation asc"""\
		.format(
			sle_conditions=get_sle_conditions(filters),
			item_conditions_sql = item_conditions_sql
		), filters, as_dict=1)

def get_items(filters):
	conditions = []
	if filters.get("item_code"):
		conditions.append("item.name=%(item_code)s")
	else:
		if filters.get("brand"):
			conditions.append("item.brand=%(brand)s")
		if filters.get("item_group"):
			conditions.append(get_item_group_condition(filters.get("item_group")))

	items = []
	if conditions:
		items = frappe.db.sql_list("""select name from `tabItem` item where {}"""
			.format(" and ".join(conditions)), filters)
	return items

def get_item_details(items, sl_entries, include_uom):
	item_details = {}
	if not items:
		items = list(set([d.item_code for d in sl_entries]))

	if not items:
		return item_details

	cf_field = cf_join = ""
	if include_uom:
		cf_field = ", ucd.conversion_factor"
		cf_join = "left join `tabUOM Conversion Detail` ucd on ucd.parent=item.name and ucd.uom=%s" \
			% frappe.db.escape(include_uom)

	res = frappe.db.sql("""
		select
			item.name, item.item_name as item_name1, item.description, item.item_group, item.brand, item.stock_uom {cf_field}
		from
			`tabItem` item
			{cf_join}
		where
			item.name in ({item_codes})
	""".format(cf_field=cf_field, cf_join=cf_join, item_codes=','.join(['%s'] *len(items))), items, as_dict=1)

	for item in res:
		item_details.setdefault(item.name, item)

	return item_details

def get_sle_conditions(filters):
	conditions = []
	if filters.get("warehouse"):
		warehouse_condition = get_warehouse_condition(filters.get("warehouse"))
		if warehouse_condition:
			conditions.append(warehouse_condition)
	if filters.get("voucher_no"):
		conditions.append("voucher_no=%(voucher_no)s")
	if filters.get("batch_no"):
		conditions.append("batch_no=%(batch_no)s")
	if filters.get("project"):
		conditions.append("project=%(project)s")

	if filters.get("team"):
		conditions.append("team=%(team)s")

	if filters.get("pmt"):
		conditions.append("pmt=%(pmt)s")

	if filters.get("ke_store"):
		conditions.append("ke_store=%(ke_store)s")

	if filters.get("sto"):
		conditions.append("sto=%(sto)s")

	if filters.get("project"):
		conditions.append("project=%(project)s")

	return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_opening_balance(filters, columns):
	if not (filters.item_code and filters.warehouse and filters.from_date):
		return

	from erpnext.stock.stock_ledger import get_previous_sle
	last_entry = get_previous_sle({
		"item_code": filters.item_code,
		"warehouse_condition": get_warehouse_condition(filters.warehouse),
		"posting_date": filters.from_date,
		"posting_time": "00:00:00"
	})
	row = {}
	row["item_code"] = _("'Opening'")
	for dummy, v in ((9, 'qty_after_transaction'), (11, 'valuation_rate'), (12, 'stock_value')):
			row[v] = last_entry.get(v, 0)

	return row

def get_warehouse_condition(warehouse):
	warehouse_details = frappe.db.get_value("Warehouse", warehouse, ["lft", "rgt"], as_dict=1)
	if warehouse_details:
		return " exists (select name from `tabWarehouse` wh \
			where wh.lft >= %s and wh.rgt <= %s and warehouse = wh.name)"%(warehouse_details.lft,
			warehouse_details.rgt)

	return ''

def get_item_group_condition(item_group):
	item_group_details = frappe.db.get_value("Item Group", item_group, ["lft", "rgt"], as_dict=1)
	if item_group_details:
		return "item.item_group in (select ig.name from `tabItem Group` ig \
			where ig.lft >= %s and ig.rgt <= %s and item.item_group = ig.name)"%(item_group_details.lft,
			item_group_details.rgt)

	return ''
