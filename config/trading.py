from __future__ import unicode_literals
from frappe import _

def get_data():
        return [
                {
			"label": _("Stock"),
			"items": [
                                {
                                        "type": "doctype",
                                        "name": "Item",
                                        "doctype": "Item",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Item Price",
                                        "doctype": "Item Price",
                                        "onboard": 1
                                },

                                {
                                        "type": "doctype",
                                        "name": "Stock Entry",
                                        "doctype": "Stock Entry",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Stock Reconcilation",
                                        "doctype": "Stock Reconcilation",
                                        "onboard": 1
                                },
                            
				{
					"type": "report",
					"is_query_report": True,
					"name": "Party Wise Stock Ledger",
					"doctype": "Stock Ledger Entry",
					"onboard": 1
				},
			        {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Stock Ledger",
                                        "doctype": "Stock Ledger Entry",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Stock Balance",
                                        "doctype": "Stock Ledger Entry",
                                        "onboard": 1
                                },

				
			]
		},
                {
                        "label": _("Selling"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Customer",
                                        "doctype": "Customer",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Sales Invoice",
                                        "doctype": "Sales Invoice",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Delivery Note",
                                        "doctype": "Delivery Note",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Sales Person",
                                        "doctype": "Sales Person",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Payment Entry",
                                        "doctype": "Payment Entry",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Sales Register",
                                        "doctype": "Sales Invoice",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Item-Wise Sales Register",
                                        "doctype": "Sales Invoice",
                                        "onboard": 1
                                },



                        ]
                },
                {
                        "label": _("Buying"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Supplier",
                                        "doctype": "Supplier",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Purchase Order",
                                        "doctype": "Purchase Order",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Purchase Reciept",
                                        "doctype": "Purchase Reciept",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Purchase Invoice",
                                        "doctype": "Purchase Invoice",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Payment Entry",
                                        "doctype": "Payment Entry",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Purchase Register",
                                        "doctype": "Purchase Invoice",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Item-Wise Purchase Register",
                                        "doctype": "Purchase Invoice",
                                        "onboard": 1
                                },


                                
                        ]
                },
                {
                        "label": _("Accounts"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Journal Entry",
                                        "doctype": "Journal Entry",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Accounts Receivable",
                                        "doctype": "Sales Invoice",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Accounts Payable",
                                        "doctype": "Purchase Invoice",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "General Ledger",
                                        "doctype": "Purchase Invoice",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Sales Tax Report",
                                        "doctype": "Sales Invoice",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "PDC Register",
                                        "doctype": "Sales Invoice",
                                        "onboard": 1
                                },

                        ]
                },
                {
                        "label": _("Financial Statement"),
                        "items": [
                                
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Trial Balance",
                                        "doctype": "GL Entry",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Profit and Loss Statement",
                                        "doctype": "GL Entry",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Balance Sheet",
                                        "doctype": "GL Entry",
                                        "onboard": 1
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Cash Flow",
                                        "doctype": "GL Entry",
                                        "onboard": 1
                                },


                        ]
                },
                {
                        "label": _("Settings"),
                        "items": [
                                {
                                        "type": "doctype",
                                        "name": "Company",
                                        "doctype": "Company",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Chart Of Accounts",
                                        "doctype": "Accounts",
                                        "onboard": 1
                                },
                                {
                                        "type": "doctype",
                                        "name": "Fiscal Year",
                                        "doctype": "Fiscal Year",
                                        "onboard": 1
                                },
                        ]
                }





        ]
