from __future__ import unicode_literals
from frappe import _

def get_data():
        return [
                {
			"label": _("Reports"),
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "PDC Register",
					"doctype": "Sales Invoice",
					"onboard": 1,
					"dependencies": ["Item"],
				},
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Sales Tax Report",
                                        "doctype": "Sales Invoice",
                                        "onboard": 1,
                                        "dependencies": ["Item"],
                                },
                                {
                                        "type": "report",
                                        "is_query_report": True,
                                        "name": "Tax Summary",
                                        "doctype": "Sales Invoice",
                                        "onboard": 1,
                                        "dependencies": ["Item"],
                                },


			    				
			]
		}
        ]
