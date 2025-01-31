// Copyright (c) 2019, Hardik Gadesha and contributors
// For license information, please see license.txt

cur_frm.add_fetch("sales_order","po_no","po_number")
cur_frm.add_fetch("sales_order","po_date","po_date")
cur_frm.add_fetch("sales_order","customer_name","customer")

frappe.ui.form.on("Warranty Certificate", "onload", function(frm) {
    // cur_frm.set_query("sales_order", function() {
    //     return {
    //         "filters": {
    //             "status": "To Bill"
    //         }
    //     };
    // });
    console.log("there")
});



frappe.ui.form.on("Warranty Certificate", {
  gate_data: function(frm) {
	cur_frm.refresh();
	cur_frm.clear_table("warranty_certificate_table");
	cur_frm.refresh_fields();
	
    frappe.call({
    "method": "group_multitech.group_multitech.doctype.warranty_certificate.warranty_certificate.insert_data",
args: {
doctype: "Warranty Certificate",
sales_order: frm.doc.sales_order
},
callback:function(r){
	var len=r.message.length;
	console.log(r)
	for (var i=0;i<len;i++){
	        var row = frm.add_child("warranty_certificate_table");
		row.item_name = r.message[i][0];
		row.delivery_date = r.message[i][1];
		row.delivery_note = r.message[i][2];
		row.qty = r.message[i][3];
	}
		cur_frm.refresh();
	}
    });
}
});
