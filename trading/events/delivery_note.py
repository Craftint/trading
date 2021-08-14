from __future__ import unicode_literals
from frappe import _

def change_autoname(doc, handler=None):
	if doc.manual_naming_series:
		doc.name = doc.manual_naming_series