# Copyright (c) 2013, Craft and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.stock.utils import update_included_uom_in_report


def execute(filters=None):
    include_uom = filters.get("include_uom")
    columns = get_columns()
    items = get_items(filters)
    sl_entries = get_stock_ledger_entries(filters, items)
    item_details = get_item_details(items, sl_entries, include_uom)
    opening_row = get_opening_balance(filters, columns)
    sales_data = sales(filters)
    data = []
    conversion_factors = []
    if opening_row:
        data.append(opening_row)

    for sle in sl_entries:
        item_detail = item_details[sle.item_code]
        party = ''
        rate = 0.00
        party_code = ''
        if sales_data.get(sle.voucher_no):
            try:
                party = sales_data[sle.voucher_no][sle.item_code][1]
                rate = sales_data[sle.voucher_no][sle.item_code][2]
                party_code = sales_data[sle.voucher_no][sle.item_code][0]
            
            except:
                pass

        if sle.actual_qty < 0:
            qty_recvd = 0.00
            rate_recvd = 0.00
            qty_issued = sle.actual_qty
            rate_issued = rate or sle.valuation_rate

        else:
            qty_recvd = sle.actual_qty
            rate_recvd = rate or sle.valuation_rate
            qty_issued = 0.00
            rate_issued = 0.00

        if 'Accounts Manager' not in frappe.get_roles(frappe.session.user) and sle.warehouse == 'Store No 6 - GE':
            rate_recvd = 0.00
            rate_issued = 0.00
            sle.stock_value = 0.00
            sle.valuation_rate = 0.00
            party = ''
            sle.voucher_type = ''
            sle.voucher_no = ''

        if filters.get('party'):

            if party_code == filters.get('party').split(',')[0]:
                                                                                                                   
                data.append([sle.date, item_detail.item_name, party, sle.voucher_type, sle.voucher_no,
                             qty_recvd, rate_recvd, qty_issued, rate_issued, sle.qty_after_transaction, sle.stock_value, sle.valuation_rate])
                                                
        else:
            data.append([sle.date, item_detail.item_name, party, sle.voucher_type, sle.voucher_no,
                         qty_recvd, rate_recvd, qty_issued, rate_issued, sle.qty_after_transaction, sle.stock_value, sle.valuation_rate])

        if include_uom:
            conversion_factors.append(item_detail.conversion_factor)

    update_included_uom_in_report(
        columns, data, include_uom, conversion_factors)
    return columns, data


def sales(filters):

    sales_data = frappe.db.sql("""select si.name,si.customer,si.customer_name,sii.rate,sii.item_code,sii.warehouse from `tabSales Invoice` si inner join `tabSales Invoice Item` sii on sii.parent = si.name where date(posting_date) between '{}' and '{}'""".format(
        filters.get("from_date"), filters.get("to_date")))

    delivery_data = frappe.db.sql("""select si.name,si.customer,si.customer_name,sii.rate,sii.item_code,sii.warehouse from `tabDelivery Note` si inner join `tabDelivery Note Item` sii on sii.parent = si.name where date(posting_date) between '{}' and '{}'""".format(
        filters.get("from_date"), filters.get("to_date")))

    purachse_data = frappe.db.sql("""select si.name,si.supplier,si.supplier_name,sii.rate,sii.item_code,sii.warehouse from `tabPurchase Receipt` si inner join `tabPurchase Receipt Item` sii on sii.parent = si.name where date(posting_date) between '{}' and '{}'""".format(
        filters.get("from_date"), filters.get("to_date")))

    purchase_inv = frappe.db.sql("""select si.name,si.supplier,si.supplier_name,sii.rate,sii.item_code,sii.warehouse from `tabPurchase Invoice` si inner join `tabPurchase Invoice Item` sii on sii.parent = si.name where date(posting_date) between '{}' and '{}'""".format(
        filters.get("from_date"), filters.get("to_date")))

    data = sales_data + delivery_data + purachse_data + purchase_inv

    a = {}
    # for item in data:
    #    a.setdefault(item[4],item)

    for item in data:
        if item[0] in a:
            x = a[item[0]]
            x.update({item[4]: [item[1], item[2], item[3]]})
            a[item[0]] = x
        else:
            a[item[0]] = {item[4]: [item[1], item[2], item[3]]}
    return a
def get_columns():
    columns = [
        {"label": _("Date"), "fieldname": "date",
         "fieldtype": "Date", "width": 95},

        {"label": _("Item Name"), "fieldname": "item_name", "width": 200},
        {"label": _("Party Name"), "fieldname": "party",
         "fieldtype": "Data", "width": 200},
        {"label": _("Voucher Type"),
         "fieldname": "voucher_type", "width": 110},

        {"label": _("Voucher No"), "fieldname": "voucher_no",
         "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},

        {"label": _("Qty Recieved"), "fieldname": "qty_recvd",
         "fieldtype": "Float", "width": 110, "convertible": "qty"},
        {"label": _("Rate Recieved At"), "fieldname": "rate_recvd", "fieldtype": "Currency", "width": 130,
         "options": "Company:company:default_currency", "convertible": "rate"},
        {"label": _("Qty Issued"), "fieldname": "qty_issued",
         "fieldtype": "Float", "width": 120, "convertible": "qty"},
        {"label": _("Rate Issued At"), "fieldname": "rate_issued", "fieldtype": "Currency", "width": 110,
         "options": "Company:company:default_currency", "convertible": "rate"},
        {"label": _("Balance Qty"), "fieldname": "qty_after_transaction",
         "fieldtype": "Float", "width": 100, "convertible": "qty"},

        {"label": _("Balance Value"), "fieldname": "stock_value", "fieldtype": "Currency", "width": 110,
         "options": "Company:company:default_currency", "convertible": "rate"},

        {"label": _("Average Rate"), "fieldname": "valuation_rate", "fieldtype": "Currency", "width": 110,
         "options": "Company:company:default_currency", "convertible": "rate"},

    ]

    return columns



def get_stock_ledger_entries(filters, items):
    item_conditions_sql = ''
    if items:
        item_conditions_sql = 'and sle.item_code in ("{}")'.format(
            ', '.join([frappe.db.escape(i) for i in items]))

    return frappe.db.sql("""select concat_ws(" ", posting_date, posting_time) as date,
			item_code, warehouse, actual_qty, qty_after_transaction, incoming_rate, valuation_rate,
			stock_value, voucher_type, voucher_no, batch_no, serial_no, company, project
		from `tabStock Ledger Entry` sle
		where company = %(company)s and
			posting_date between %(from_date)s and %(to_date)s
			{sle_conditions}
			{item_conditions_sql}
			order by posting_date asc, posting_time asc, creation asc"""
                         .format(
                             sle_conditions=get_sle_conditions(filters),
                             item_conditions_sql=item_conditions_sql
                         ), filters, as_dict=1)


def get_items(filters):
    conditions = []
    if filters.get("item_code"):
        conditions.append("item.name=%(item_code)s")
    else:
        if filters.get("brand"):
            conditions.append("item.brand=%(brand)s")
        if filters.get("item_group"):
            conditions.append(get_item_group_condition(
                filters.get("item_group")))

    items = []
    if conditions:
        items = frappe.db.sql_list("""select name from `tabItem` item where {}"""
                                   .format(" and ".join(conditions)), filters)
    return items


def get_item_details(items, sl_entries, include_uom):
    item_details = {}
    if not items:
        items = list(set([d.item_code for d in sl_entries]))

    if not items:
        return item_details

    cf_field = cf_join = ""
    if include_uom:
        cf_field = ", ucd.conversion_factor"
        cf_join = "left join `tabUOM Conversion Detail` ucd on ucd.parent=item.name and ucd.uom='%s'" \
            % frappe.db.escape(include_uom)

    res = frappe.db.sql("""
		select
			item.name, item.item_name, item.description, item.item_group, item.brand, item.stock_uom {cf_field}
		from
			`tabItem` item
			{cf_join}
		where
			item.name in ({item_codes})
	""".format(cf_field=cf_field, cf_join=cf_join, item_codes=','.join(['%s'] * len(items))), items, as_dict=1)

    for item in res:
        item_details.setdefault(item.name, item)

    return item_details


def get_sle_conditions(filters):
    conditions = []
    if filters.get("warehouse"):
        warehouse_condition = get_warehouse_condition(filters.get("warehouse"))
        if warehouse_condition:
            conditions.append(warehouse_condition)
    if filters.get("voucher_no"):
        conditions.append("voucher_no=%(voucher_no)s")
    if filters.get("batch_no"):
        conditions.append("batch_no=%(batch_no)s")
    if filters.get("project"):
        conditions.append("project=%(project)s")

    return "and {}".format(" and ".join(conditions)) if conditions else ""


def get_opening_balance(filters, columns):
    if not (filters.item_code and filters.warehouse and filters.from_date):
        return

    from erpnext.stock.stock_ledger import get_previous_sle
    last_entry = get_previous_sle({
        "item_code": filters.item_code,
        "warehouse_condition": get_warehouse_condition(filters.warehouse),
        "posting_date": filters.from_date,
        "posting_time": "00:00:00"
    })
    row = {}
    row["item_code"] = _("'Opening'")
    for dummy, v in ((9, 'qty_after_transaction'), (11, 'valuation_rate'), (12, 'stock_value')):
        row[v] = last_entry.get(v, 0)

    return row


def get_warehouse_condition(warehouse):
    warehouse_details = frappe.db.get_value(
        "Warehouse", warehouse, ["lft", "rgt"], as_dict=1)
    if warehouse_details:
        return " exists (select name from `tabWarehouse` wh \
			where wh.lft >= %s and wh.rgt <= %s and warehouse = wh.name)" % (warehouse_details.lft,
                                                                    warehouse_details.rgt)

    return ''


def get_item_group_condition(item_group):
    item_group_details = frappe.db.get_value(
        "Item Group", item_group, ["lft", "rgt"], as_dict=1)
    if item_group_details:
        return "item.item_group in (select ig.name from `tabItem Group` ig \
			where ig.lft >= %s and ig.rgt <= %s and item.item_group = ig.name)" % (item_group_details.lft,
                                                                          item_group_details.rgt)

    return ''
