// Copyright (c) 2016, Craft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Murjan Stock Ledger"] = {
	"filters": [
	  {
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			"fieldname":"item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"get_query": function() {
				return {
					query: "erpnext.controllers.queries.item_query"
				}
			},
		},
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group"
		},
		{
			"fieldname":"batch_no",
			"label": __("Batch No"),
			"fieldtype": "Link",
			"options": "Batch"
		},
		{
			"fieldname":"brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"options": "Brand"
		},
		{
			"fieldname":"voucher_no",
			"label": __("Voucher #"),
			"fieldtype": "Data"
		},
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldname":"include_uom",
			"label": __("Include UOM"),
			"fieldtype": "Link",
			"options": "UOM"
		},
		{
			"fieldname":"party_type",
			"label": __("Party Type"),
			"fieldtype": "Link",
			"options": "Party Type",
			"default": "",
			on_change: function() {
				frappe.query_report.set_filter_value('party', "");
			}
		},
	        {
                        "fieldname":"party",
                        "label": __("Party"),
                        "fieldtype": "MultiSelectList",
                        get_data: function(txt) {
                                if (!frappe.query_report.filters) return;

                                let party_type = frappe.query_report.get_filter_value('party_type');
                                if (!party_type) return;

                                return frappe.db.get_link_options(party_type, txt);
                        },
                        on_change: function() {
                                var party_type = frappe.query_report.get_filter_value('party_type');
                                var parties = frappe.query_report.get_filter_value('party');

                                if(!party_type || parties.length === 0 || parties.length > 1) {
                                        frappe.query_report.set_filter_value('party_name', "");
                                        frappe.query_report.set_filter_value('tax_id', "");
                                        return;
                                } else {
                                        var party = parties[0];
                                        var fieldname = erpnext.utils.get_party_name(party_type) || "name";
                                        frappe.db.get_value(party_type, party, fieldname, function(value) {
                                                frappe.query_report.set_filter_value('party_name', value[fieldname]);
                                        });

                                        if (party_type === "Customer" || party_type === "Supplier") {
                                                frappe.db.get_value(party_type, party, "tax_id", function(value) {
                                                        frappe.query_report.set_filter_value('tax_id', value["tax_id"]);
                                                });
                                        }
                                }
			}
		},

		{
			"fieldname":"party_name",
			"label": __("Party Name"),
			"fieldtype": "Data",
			"hidden": 1
		},
	],
	onload: function(report) {
		report.page.add_inner_button(__("Search Items"), function() {
			var filters = report.get_values();
			  
			  console.log(report) 
                          new frappe.ui.form.LinkSelector({
                                        doctype: "Item",
                                        fieldname: filters.item_code,
                                        target:report.filters[4]
			  });

		});
	}
   
};

