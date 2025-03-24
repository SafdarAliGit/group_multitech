frappe.ui.form.on("Sales Invoice Item", "shift", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	if (d.shift == 'Day'){
		cur_frm.add_fetch("daily_wages_labour","total_duties_in_days","qty")	
	}
});

frappe.ui.form.on("Sales Invoice Item", "shift", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	if (d.shift == 'Night'){
		cur_frm.add_fetch("daily_wages_labour","total_duties_in_nights","qty")	
	}
});

frappe.ui.form.on("Sales Invoice Item", "shift", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	if (d.shift == 'Holiday'){
		cur_frm.add_fetch("daily_wages_labour","total_duties_in_holidays","qty")	
	}
});

