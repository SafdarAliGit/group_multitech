// Copyright (c) 2016, Hardik Gadesha and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Invoice Payment"] = {
	"filters": [
		{
			"fieldname":"company ",
			"label": "Comapny",
			"fieldtype": "Link",
			"width": "100",
			"options": "Company",
			"default": "Multitech Engineers"
		},

		{
			"fieldname":"invoice_from_date",
			"label": "Commercial Invoice Date",
			"fieldtype": "Date",
			"width": "100",
			// "default": frappe.datetime.start_month(),

		},


		// {
		// 	"fieldname":"invoice_to_date",
		// 	"label": "Commercial Invoice to Date",
		// 	"fieldtype": "Date",
		// 	"width": "100",
		// 	// "default": frappe.datetime.start_end(),
		// },


		{
			"fieldname":"sales_tax_invoice_from_date",
			"label": "Sales tax Invoice Date",
			"fieldtype": "Date",
			"width": "100",
			// "default": frappe.datetime.start_month(),

		},


		// {
		// 	"fieldname":"sales_tax_invoice_to_date",
		// 	"label": "Payment Entry Date",
		// 	"fieldtype": "Date",
		// 	"width": "100",
		// 	// "default": frappe.datetime.start_end(),
		// },



		// {
		// 	"fieldname":"from_date",
		// 	"label": __("From Date"),
		// 	"fieldtype": "Date",
		// 	"width": "100",
		// 	"default": frappe.datetime.get_today(),
		// },
		// {
		// 	"fieldname":"to_date",
		// 	"label": __("To Date"),
		// 	"fieldtype": "Date",
		// 	"width": "100",
		// 	"default": frappe.datetime.get_today(),
		// },


	]
};
