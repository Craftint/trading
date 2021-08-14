# Copyright (c) 2013, Craft and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    sales_data = frappe.db.sql('''select 
                        'Customer' as party_type,
                        customer_name,
                        po_no,
			tax_id,
			name,
			posting_date,
                        total,
                        discount_amount,
			net_total,
			total_taxes_and_charges,
			grand_total
		from `tabSales Invoice` si
			where date(posting_date) BETWEEN "{}" and "{}" and docstatus = 1 Order by date(posting_date) ASC'''.format(filters.get("from_date"), filters.get("to_date")))

    purchase_data = frappe.db.sql('''select supplier_name,
                        'Supplier' as party_type,
                        bill_no,
			tax_id,
			name,
			posting_date,
                        total,
                        discount_amount,
			net_total,
			total_taxes_and_charges,
			grand_total
		from `tabPurchase Invoice` 
			where date(posting_date) BETWEEN "{}" and "{}" and docstatus = 1 Order by date(posting_date) ASC'''.format(filters.get("from_date"), filters.get("to_date")))

    """journal_data = frappe.db.sql('''select je.supplier,
                        je.tax_id,
                        je.tax_bill_no,
                        je.tax_bill_date,
                        je.total_debit,
                        jea.debit,
			je.total_debit
                from `tabJournal Entry` je
			inner join `tabJournal Entry Account` jea
		on je.name = jea.parent
                        where date(je.posting_date) BETWEEN "{}" and "{}" and je.docstatus = 1 and jea.account = "60002 - Vat Output Account - GE" and je.supplier <> "" '''.format(filters.get("from_date"),filters.get("to_date"))) """

    if filters.get("entry_type") == "Sales Invoice":
        data = sales_data
    elif filters.get("entry_type") == "Purchase Invoice":
        data = purchase_data

    return columns, data


def get_columns():
    return [
        _("Party Type") + ":Data:120",
        _("Party") + ":Data:120",
        _("Bill No") + ":Data:120",
        _("TRN") + ":Data:120",
        _("INV No") + ":Link/Sales Invoice:120",
        _("INV Date") + ":Date:160",
        _("Gross") + ":Currency:120",
        _("Discount") + ":Currency:120",
        _("Net Amount") + ":Currency:120",
        _("Vat") + ":Currency:120",
        _("Total") + ":Currency:100",
    ]
