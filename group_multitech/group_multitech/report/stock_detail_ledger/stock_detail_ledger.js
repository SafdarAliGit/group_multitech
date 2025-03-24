// Copyright (c) 2016, Hardik Gadesha and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Detail Ledger"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Company",
			"default": frappe.defaults.get_user_default("company"),
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "100",
			"default": frappe.datetime.month_start()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "100",
			"default": frappe.datetime.month_end()
		},
		{
			"fieldname":"item_code",
			"label": __("Item Code"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Item"
		},
		{
			"fieldname":"team",
			"label": __("Team"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Team",
			get_query: () => {
				return {
					query: "group_multitech.group_multitech.report.stock_detail.stock_detail.team_query",
				};
			}
		},
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Project"
		},
		{
			"fieldname":"pmt",
			"label": __("PMT"),
			"fieldtype": "Link",
			"width": "100",
			"options": "PMT"
		},
		{
			"fieldname":"ke_store",
			"label": __("KE Store"),
			"fieldtype": "Link",
			"width": "100",
			"options": "KE Store"
		},
		{
			"fieldname":"sto",
			"label": __("STO"),
			"fieldtype": "Link",
			"width": "100",
			"options": "STO"
		},
	]
};
