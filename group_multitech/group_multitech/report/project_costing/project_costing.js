// Copyright (c) 2016, Hardik Gadesha and contributors
// For license information, please see license.txt
/* eslint-disable */
var d = new Date();
frappe.query_reports["Project Costing"] = {
	
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("company")
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "100",
			"default": new Date(d.getFullYear(),d.getMonth(),1),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "100",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			"width": "100",
			get_data: function(txt) {
				return frappe.db.get_link_options('Project', txt);
			}
		},
		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "MultiSelectList",
			"width": "100",
			get_data: function(txt) {
				return frappe.db.get_link_options('Cost Center', txt);
			}
		},
		{
			"fieldname":"account_withholding",
			"label": __("Withholding Account"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Account",
			"default": "2304 - SST WHT 20% - ME",
			"reqd":1,
			get_query: function() {
				return {
					filters: [
						["Account", "company", "=", frappe.query_report.get_filter_value('company')],
						["Account", "account_type", "in", ["Tax", "Chargeable", "Expense Account"]]
					]
				}
			},
		},
	]
};
