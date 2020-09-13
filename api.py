# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import json
import frappe, erpnext
from frappe import _, scrub


@frappe.whitelist(allow_guest=True)
def cancel_doc():
    doc = frappe.get_doc('Stock Reconciliation', 'MAT-RECO-2020-00023')
    doc.cancel()
    frappe.db.commit()
