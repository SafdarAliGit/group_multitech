import frappe

def custom_validation(doc, event):
    if doc.company == 'Multitech Engineers' and doc.customer == 'K-Electric Limited':
        if doc.cost_center != 'Industrial Projects - ME':
            if not doc.customer_contract:
                frappe.throw('Customer Contract is mandatory')
            else:
                doc.customer_contract = 1