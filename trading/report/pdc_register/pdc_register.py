# Copyright (c) 2013, Craft and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint


def execute(filters=None):
    columns = get_columns()
    cond = ''
    if filters.get('payment_type'):
        cond = "and payment_type = '{}'".format(filters.get('payment_type'))

    data = frappe.db.sql("""select name,payment_type,party_type,party_name,bank_account,reference_no,reference_date,paid_amount from `tabPayment Entry` where date(reference_date) > CURDATE() and docstatus != 2 {}""".format(cond))
    return columns, data


def get_columns():
    return [
        {
            "label": _("Payment Entry"),
            "fieldname": "payment_entry",
            "fieldtype": "Link",
            "options": "Payment Entry",
            "width": 120
        },

        {
            "label": _("Payment Type"),
            "fieldname": "payment_type",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Party Type"),
            "fieldname": "party_type",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Party Name"),
            "fieldname": "party_name",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Bank Account"),
            "fieldname": "bank_account",
            "fieldtype": "Data",
            "width": 120
        },


        {
            "label": _("Cheque No"),
            "fieldname": "cheque_no",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Cheque Date"),
            "fieldname": "cheque_date",
            "fieldtype": "Date",
            "width": 120
        },

        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120
        }
    ]
