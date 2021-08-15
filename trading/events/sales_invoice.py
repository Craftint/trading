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

@frappe.whitelist()
def change_autoname_and_remarks_after_save(**args):
	"""
	maped the manual autoname and remarks in delivery note
	"""
	if args.get("manual_naming_series"):
		is_exist = frappe.db.exists("Sales Invoice", args.get("name"))
		if is_exist:
			frappe.db.sql("""
				update `tabSales Invoice` 
					set name = "{manual_naming_series}",
					manual = 1
					where name = "{name}";""".format(
						name = is_exist, 
						manual_naming_series = args.get("manual_naming_series")))
			frappe.db.commit()
			frappe.db.sql("""
				update `tabSales Invoice Item` 
					set parent = "{manual_naming_series}" 
					where parent = "{name}";""".format(
						name = is_exist, 
						manual_naming_series = args.get("manual_naming_series")))
			frappe.db.commit()
	return True

@frappe.whitelist()
def check_if_manual_and_manual_series_exist(**args):
	"""
	check the manual exist
	"""
	if args.get("name"):
		return frappe.db.sql("""
						select 
							tsi.manual, 
							tsi.manual_naming_series 
						from 
							`tabSales Invoice` tsi 
						where 
							tsi.name = "{name}";""".format(
							name = args.get("name")), as_dict=True)
	else:
		return {}						
