from __future__ import unicode_literals
from frappe import _

def get_data():
        return [
                {
			"label": _("Stock Reports"),
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Party Wise Stock Ledger",
					"doctype": "Stock Ledger Entry",
					"onboard": 1,
					"dependencies": ["Item"],
				},
			    				
			]
		}
        ]
