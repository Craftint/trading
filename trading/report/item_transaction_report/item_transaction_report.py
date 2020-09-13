# Copyright (c) 2013, Craft and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    condition = ''

    if filters.get("item"):
        condition = "where item_code = '{}'".format(filters.get("item"))

    stock_opening = frappe.db.sql(
        """select creation,'Opening Stock' as party,'Opening Stock' as supplier_name,name,item_code,item_code,actual_qty,valuation_rate,valuation_rate*actual_qty from `tabBin` {}""")

    purchase_data = frappe.db.sql(
        """select posting_date,'Supplier' as party,supplier_name,tp.name,item_code,item_name,qty,rate,amount from `tabPurchase Invoice` tp inner join `tabPurchase Invoice Item` tpi on tp.name = tpi.parent where tp.docstatus = 1 and is_opening = 'No' {}""".format(condition))

    i
    sales_data = frappe.db.sql("""select posting_date,'Customer' as party,customer_name,tp.name,item_code,item_name,qty,rate,amount from `tabSales Invoice` tp inner join `tabSales Invoice Item` tpi on tp.name = tpi.parent where tp.docstatus = 1 and is_opening = 'No' {}""".format(condition))

    data = stock_opening + purchase_data + sales_data

    return columns, data


def get_columns():
    return [
        _("Date") + ":Date:150",
        _("Party Type") + ":Data:200",
        _("Party") + ":Data:200",
        _("Voucher No") + ":Data:200",
        _("Item Code") + ":Data:120",
        _("Item Name") + ":Data:200",
        _("Qty") + ":Float:160",
        _("Rate") + ":Currency:120",
        _("Amount") + ":Currency:120",

    ]
