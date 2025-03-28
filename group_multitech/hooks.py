# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "group_multitech"
app_title = "Group Multitech"
app_publisher = "Hardik Gadesha"
app_description = "Application For Group Multitech"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hardikgadesha@gmail.com"
app_license = "MIT"


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/group_multitech/css/group_multitech.css"
# app_include_js = "/assets/group_multitech/js/group_multitech.js"

# include js, css files in header of web template
# web_include_css = "/assets/group_multitech/css/group_multitech.css"
# web_include_js = "/assets/group_multitech/js/group_multitech.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "group_multitech.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "group_multitech.install.before_install"
# after_install = "group_multitech.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "group_multitech.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Stock Ledger Entry": {
		"validate": "group_multitech.custom_changes.sle_validate"
	},
    "Sales Invoice":{
        "validate": "group_multitech.overrides.sales_invoice.custom_validation"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"group_multitech.tasks.all"
# 	],
# 	"daily": [
# 		"group_multitech.tasks.daily"
# 	],
# 	"hourly": [
# 		"group_multitech.tasks.hourly"
# 	],
# 	"weekly": [
# 		"group_multitech.tasks.weekly"
# 	]
# 	"monthly": [
# 		"group_multitech.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "group_multitech.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "group_multitech.event.get_events"
# }
