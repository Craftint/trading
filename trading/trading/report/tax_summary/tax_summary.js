// Copyright (c) 2016, Craft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Tax Summary"] = {
	"filters": [
		 {
                        "fieldname":"from_date",
                        "label": __("From Date"),
                        "fieldtype": "Date",
                        'reqd': 1,
                        "default": frappe.datetime.month_start()
                },
                {
                        "fieldname":"to_date",
                        "label": __("To Date"),
                        "fieldtype": "Date",
                        'reqd': 1,
                        "default":frappe.datetime.month_end()
                },
	]
};
