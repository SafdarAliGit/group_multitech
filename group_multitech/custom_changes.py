import frappe


def sle_validate(self, method):
	if self.voucher_type == "Stock Entry":
		self.team = frappe.db.get_value(self.voucher_type, self.voucher_no, "team")
		self.pmt = frappe.db.get_value(self.voucher_type, self.voucher_no, "pmt")
		self.ke_store = frappe.db.get_value(self.voucher_type, self.voucher_no, "ke_store")
		self.sto = frappe.db.get_value(self.voucher_type, self.voucher_no, "sto")


@frappe.whitelist()
def update_sles():
	# data = frappe.db.sql("""select name, voucher_type, voucher_no from `tabStock Ledger Entry`""")
	# for d in data:
	# 	if d[1] == "Stock Entry":
	# 		ste = frappe.get_doc(d[1], d[2])
	# 		frappe.db.sql("""update `tabStock Ledger Entry` set team = '{}', pmt = '{}', ke_store = '{}', sto = '{}' where 
	# 			name = '{}'""".format(ste.team, ste.pmt, ste.ke_store, ste.sto, d[0]))

	frappe.db.sql("""update `tabStock Ledger Entry` set team = NULL where 
				team = 'None'""")