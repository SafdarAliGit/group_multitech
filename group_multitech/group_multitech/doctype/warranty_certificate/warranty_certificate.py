# -*- coding: utf-8 -*-
# Copyright (c) 2019, Hardik Gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class WarrantyCertificate(Document):
	pass

@frappe.whitelist(allow_guest=True)
def insert_data(doctype, sales_order):
	query="select obj2.item_name, obj1.posting_date, obj1.name, obj2.qty from `tabDelivery Note` obj1, `tabDelivery Note Item` obj2 where obj1.name = obj2.parent and obj2.against_sales_order = '"+str(sales_order)+"';"
	li=[]
	dic=frappe.db.sql(query, as_dict=True)
	for i in dic:	
		item_name,posting_date,name,qty=i['item_name'],i['posting_date'],i['name'],i['qty']
		li.append([item_name,posting_date,name,qty])
	return li
