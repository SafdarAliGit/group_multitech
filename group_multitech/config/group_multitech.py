from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Stock"),
			"items": [
				{
					"type": "doctype",
					"name": "Stock Entry",
					"onboard":1
				},
				{
					"type": "doctype",
					"name": "Team",
					"onboard":1
				},
				{
					"type": "doctype",
					"name": "Project",
					"onboard":1
				},
				{
					"type": "doctype",
					"name": "PMT",
					"onboard":1
				},
				{
					"type": "doctype",
					"name": "KE Store",
					"onboard":1
				},
				{
					"type": "doctype",
					"name": "STO",
					"onboard":1
				},
				{
					"type": "report",
					"name": "Stock Detail",
					"doctype": "Stock Entry",
					"is_query_report": True,
					"onboard": 1,
				},
				{
					"type": "report",
					"name": "Stock Detail By Date",
					"doctype": "Stock Entry",
					"is_query_report": True,
					"onboard": 1,
				},
				{
					"type": "report",
					"name": "Stock Detail Ledger",
					"doctype": "Stock Entry",
					"is_query_report": True,
					"onboard": 1,
				},
				{
					"type": "report",
					"name": "Project Costing",
					"doctype": "Project",
					"is_query_report": True,
					"onboard": 1,
				},
			]
		},
		{
			"label": _("Daily Wages Labour"),
			"items": [
				{
					"type": "doctype",
					"name": "Daily Wages Labour Year Master",
				},
				{
					"type": "doctype",
					"name": "Daily Wages Labour Month Master",
				},
				{
					"type": "doctype",
					"name": "Cluster",
				},
				{
					"type": "doctype",
					"name": "Daily Wages Labour"
				}
				
			]
		},
		{
			"label": _("Customer Contract Masters"),
			"items": [
				{
					"type": "doctype",
					"name": "Customer Contract",
				},
				{
					"type": "doctype",
					"name": "Company Enlistment",
				}
			]
		},
		{
			"label": _("Warranty"),
			"items": [
				{
					"type": "doctype",
					"name": "Warranty Certificate"
				}
			]
		}
	]
