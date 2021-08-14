from __future__ import unicode_literals
from frappe import _

def change_autoname(doc, handler=None):
	"""
	maped the manual autoname in delivery note
	"""
	if doc.manual_naming_series and doc.is_new():
		doc.name = doc.manual_naming_series
		for item in doc.items:
			item.parent = doc.manual_naming_series