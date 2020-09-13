# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "trading"
app_title = "Trading"
app_publisher = "Craft"
app_description = "App for Trading companies"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hafees@craftinteractive.ae"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/trading/css/trading.css"
# app_include_js = "/assets/trading/js/trading.js"

# include js, css files in header of web template
# web_include_css = "/assets/trading/css/trading.css"
# web_include_js = "/assets/trading/js/trading.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Invoice" : "public/js/sales_invoice.js","Purchase Order":"public/js/purchase_order.js","Delivery Note":"public/js/delivery_note.js","Purchase Invoice":"public/js/purchase_invoice.js","Quotation" : "public/js/quotation.js",}
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
# get_website_user_home_page = "trading.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "trading.install.before_install"
# after_install = "trading.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "trading.notifications.get_notification_config"

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

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Company-warehouse",
                    "Company-sales_taxes_and_charges",
                    "Company-purchase_taxes_and_charges",
                    "Sales Invoice-delivery_note",
                    "Sales Invoice-last_transaction_details",
                    "Sales Invoice-previous_transaction",
                    "Delivery Note-last_transaction_details",
                    "Delivery Note-previous_transaction",
                    "Purchase Receipt-purchase_receipt"

                ]
            ]
        ]
    },
    {
        "doctype": "Property Setter",
        "filters": [
            [
                "name",
                "in",
                [
                    "Sales Invoice-accounting_dimensions_section-hidden",
                    "Sales Invoice-currency_and_price_list-hidden",
                    "Sales Invoice-packing_list-hidden",
                    "Sales Invoice-time_sheet_list-hidden",
                    "Sales Invoice-loyalty_points_redemption-hidden",
                    "Sales Invoice-payments_section-hidden",
                    "Sales Invoice-column_break4-column_break4",
                    "Sales Invoice-vat_section-hidden",
                    "Sales Invoice-more_information-hidden",
                    "Sales Invoice-subscription_section-hidden",
                    "Delivery Note-transporter_info-hidden",
                    "Delivery Note-more_info-hidden",
                    "Delivery Note-section_break_83-hidden",
                    "Delivery Note-subscription_section-hidden",
                    "Delivery Note-sales_team_section_break-hidden",
                    "Delivery Note-section_break1-hidden",
                    "Purchase Order-Subscription Section-hidden",
                    "Purchase Order-ref_sq-hidden-hidden",
                    "Purchase Invoice-write_off-hidden",
                    "Purchase Invoice-subscription_section-hidden"
                ]
            ]
        ]
    }

                    
]


#doc_events = {
# 	"Sales Invoice": {
# 		"validate": "trading.trading.sales_invoice.validate_sales_person",
#        }
#}
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"trading.tasks.all"
# 	],
# 	"daily": [
# 		"trading.tasks.daily"
# 	],
#}
