from __future__ import unicode_literals
from frappe import _
import frappe
from frappe.utils import formatdate

def change_autoname_and_remarks(doc, handler=None):
	"""
	check and change autoname remarks
	"""
	if doc.manual_naming_series and doc.is_new():
		doc.name = doc.manual_naming_series
		for item in doc.items:
			item.parent = doc.manual_naming_series
	if not doc.remarks:
			if doc.po_no and doc.po_date:
				doc.remarks = _("Against Customer Order {0} dated {1}").format(doc.po_no,
					formatdate(doc.po_date))
			else:
				doc.remarks = _("No Remarks")    