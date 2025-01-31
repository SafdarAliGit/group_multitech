frappe.ui.form.on("Sales Invoice", {
    customer_contract(frm) {
        if(frm.doc.customer_contract) {
            frappe.call({
                method: "fetch_price_list",
                doc: frm.doc,
                callback(r) {
                    if(r.message) {
                        frm.set_value("selling_price_list", r.message);
                    }
                }
            })
        } else {
            frm.set_value("selling_price_list", "");
        }
    }
})