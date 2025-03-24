frappe.ui.form.on("Sales Invoice", {
    "sales_tax": function(frm) {
        frappe.call({
		"method": "group_multitech.group_multitech.sales_tax_series.sales_tax_series",
		args: {
			sales_tax: frm.doc.sales_tax,
			company: frm.doc.company
		},
		callback:function(r){
		var myJSON = JSON.stringify(r);
		var myJSONnew = myJSON.match(/\d+/g).map(Number);
		msgprint("In Company " +frm.doc.company+ " Last Series of " +frm.doc.sales_tax+ " is : " +frm.doc.sales_tax+ " - " + myJSONnew )
		;}
	});
    }
});

frappe.ui.form.on("Sales Invoice", {
    "company": function(frm) {
        frappe.call({
		"method": "group_multitech.group_multitech.sales_tax_series.sales_tax_series",
		args: {
			sales_tax: frm.doc.sales_tax,
			company: frm.doc.company
		},
		callback:function(r){
		var myJSON = JSON.stringify(r);
		var myJSONnew = myJSON.match(/\d+/g).map(Number);
		msgprint("In Company " +frm.doc.company+ " Last Series of " +frm.doc.sales_tax+ " is : " +frm.doc.sales_tax+ " - " + myJSONnew )
		;}
	});
    }
});

frappe.ui.form.on("Sales Invoice", {
    "tax_number": function(frm) {
        frappe.call({
		"method": "group_multitech.group_multitech.sales_tax_series.sales_tax_series",
		args: {
			sales_tax: frm.doc.sales_tax,
			company: frm.doc.company
		},
		callback:function(r){
		var myJSON = JSON.stringify(r);
		var myJSONnew = myJSON.match(/\d+/g).map(Number);
		if(myJSONnew == frm.doc.tax_number){
			msgprint("In Company " +frm.doc.company+ ", Series of " +frm.doc.sales_tax+ " : " +frm.doc.sales_tax+ " - " + myJSONnew + " is Already Exist")
		}
		;}
	});
    }
});
