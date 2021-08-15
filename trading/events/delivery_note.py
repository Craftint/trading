from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.selenium_testdriver import TestDriver

@frappe.whitelist()
def change_autoname_after_save(**args):
	"""
	maped the manual autoname in delivery note
	"""
	if args.get("manual_naming_series"):
		is_exist = frappe.db.exists("Delivery Note", args.get("name"))
		if is_exist:
			frappe.db.sql("""
				update `tabDelivery Note` 
					set name = "{manual_naming_series}",
					manual = 1,
					manual_naming_series = "{manual_naming_series}"
					where name = "{name}";""".format(
						name = is_exist, 
						manual_naming_series = args.get("manual_naming_series")))
			frappe.db.commit()
			frappe.db.sql("""
				update `tabDelivery Note Item` 
					set parent = "{manual_naming_series}" 
					where parent = "{name}";""".format(
						name = is_exist, 
						manual_naming_series = args.get("manual_naming_series")))
			frappe.db.commit()
	return True

def change_autoname_new_form(doc, handler=None):
	"""
	change name for new form
	"""
	if doc.manual_naming_series and doc.is_new():
		doc.name = doc.manual_naming_series
		for item in doc.items:
			item.parent = doc.manual_naming_series
