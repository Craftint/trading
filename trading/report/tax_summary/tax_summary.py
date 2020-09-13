# Copyright (c) 2013, Craft and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = frappe.db.sql("""select voucher_type,voucher_no,account,posting_date,debit,credit from `tabGL Entry` where date(posting_date) BETWEEN '{}' and '{}' and account in ('60002 - Vat Output Account - GE','60001 - VAT Input A/c - GE')""".format(filters.get("from_date"), filters.get("to_date")))
    return columns, data


def get_columns():
    return [
        _("Voucher Type") + ":Data:120",
        _("Voucher No") + ":Data:200",
        _("Account") + ":Data:200",
        _("Posting Date") + ":Date:120",
        _("Debit") + ":Currency:120",
        _("Credit") + ":Currency:120",

    ]
