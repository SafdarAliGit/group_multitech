// Copyright (c) 2018, Hardik Gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Wages Labour Table", "day", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var wages = frm.doc.daily_wages_labour_table;
	var day = 0;
   	for(var j in wages) {
		day = day + wages[j].day;
		cur_frm.set_value("total_duties_in_days",day);
		var in_12hrs = day * 1.5;
		cur_frm.set_value("total_duties_in_days_12_hrs",in_12hrs);
	}	
});

frappe.ui.form.on("Daily Wages Labour Table", "night", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var wages = frm.doc.daily_wages_labour_table;
	var night = 0;
   	for(var j in wages) {
		night = night + wages[j].night;
		cur_frm.set_value("total_duties_in_nights",night);
		var in_12hrs = night * 1.5;
		cur_frm.set_value("total_duties_in_nights_12_hrs",in_12hrs);
	}	
});

frappe.ui.form.on("Daily Wages Labour Table", "holiday", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var wages = frm.doc.daily_wages_labour_table;
	var holiday = 0;
   	for(var j in wages) {
		holiday = holiday + wages[j].holiday;
		cur_frm.set_value("total_duties_in_holidays",holiday);
		var in_12hrs = holiday * 1.5;
		cur_frm.set_value("total_duties_in_holidays_12_hrs",in_12hrs);
	}	
});

frappe.ui.form.on("Daily Wages Labour Table", "daily_wages_labour_table_remove", function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var wages = frm.doc.daily_wages_labour_table;
	var day = 0;
	var night = 0;
	var holiday = 0;
   	for(var j in wages) {
		day = day + wages[j].day;
		night = night + wages[j].night;
		holiday = holiday + wages[j].holiday;
		var in_12hrs_day = day * 1.5;
		var in_12hrs_night = night * 1.5;
		var in_12hrs_holiday = holiday * 1.5;
		cur_frm.set_value("total_duties_in_days",day);
		cur_frm.set_value("total_duties_in_nights",night);
		cur_frm.set_value("total_duties_in_holidays",holiday);
		cur_frm.set_value("total_duties_in_days_12_hrs",in_12hrs_day);
		cur_frm.set_value("total_duties_in_nights_12_hrs",in_12hrs_night);
		cur_frm.set_value("total_duties_in_holidays_12_hrs",in_12hrs_holiday);
	}	
});
