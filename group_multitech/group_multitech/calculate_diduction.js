cur_frm.add_fetch("item_code","cost_of_one_inch_of_excavation","cost_of_one_inch_of_excavation")
cur_frm.add_fetch("item_code","deduction_formula","deduction_formula")

frappe.ui.form.on("Sales Invoice Item", "cost_of_one_inch_of_excavation", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	frappe.model.set_value(d.doctype, d.name, "inches_not_excavated", (39 - d.actual_depth_excavated ));
	frappe.model.set_value(d.doctype, d.name, "cost_of_inches_not_excavated",(d.inches_not_excavated * d.cost_of_one_inch_of_excavation));
	var temp = d.qty * d.cost_of_inches_not_excavated
	frappe.model.set_value(d.doctype, d.name, "less_amount",Math.round(temp));
	
	var item_table = frm.doc.items;
	var less_amount = 0;
   	for(var j in item_table) {
		less_amount = less_amount + item_table[j].less_amount;
		cur_frm.set_value("discount_amount",less_amount);
	}
});

frappe.ui.form.on("Sales Invoice Item", "actual_depth_excavated", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	frappe.model.set_value(d.doctype, d.name, "inches_not_excavated", (39 - d.actual_depth_excavated ));
	frappe.model.set_value(d.doctype, d.name, "cost_of_inches_not_excavated",(d.inches_not_excavated * d.cost_of_one_inch_of_excavation));
	var temp = d.qty * d.cost_of_inches_not_excavated
	frappe.model.set_value(d.doctype, d.name, "less_amount",Math.round(temp));

	var item_table = frm.doc.items;
	var less_amount = 0;
   	for(var j in item_table) {
		less_amount = less_amount + item_table[j].less_amount;
		cur_frm.set_value("discount_amount",less_amount);
	}	
});

frappe.ui.form.on("Sales Invoice Item", "qty", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	frappe.model.set_value(d.doctype, d.name, "inches_not_excavated", (39 - d.actual_depth_excavated ));
	frappe.model.set_value(d.doctype, d.name, "cost_of_inches_not_excavated",(d.inches_not_excavated * d.cost_of_one_inch_of_excavation));
	var temp = d.qty * d.cost_of_inches_not_excavated
	frappe.model.set_value(d.doctype, d.name, "less_amount",Math.round(temp));

	var item_table = frm.doc.items;
	var less_amount = 0;
   	for(var j in item_table) {
		less_amount = less_amount + item_table[j].less_amount;
		cur_frm.set_value("discount_amount",less_amount);
	}
});

