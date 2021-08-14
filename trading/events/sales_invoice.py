from __future__ import unicode_literals
from frappe import _
from frappe.utils import formatdate

def change_autoname_and_remarks(doc, handler=None):
	if doc.manual_naming_series:
		doc.name = doc.manual_naming_series
	if not doc.remarks:
			if doc.po_no and doc.po_date:
				doc.remarks = _("Against Customer Order {0} dated {1}").format(doc.po_no,
					formatdate(doc.po_date))
			else:
				doc.remarks = _("No Remarks")    