import frappe
from erpnext.stock.utils import get_latest_stock_qty

@frappe.whitelist()
def get_last_selling_price_of_customer(item_code = '',customer = ''):
    
    last_customer_price = frappe.db.sql("""select rate,posting_date from `tabSales Invoice Item` sid inner join `tabSales Invoice` si on sid.parent= si.name where si.customer = '{}' and sid.item_code = '{}' and si.docstatus != 2 order by si.posting_date DESC""".format(customer,item_code))
    if last_customer_price:
        last_customer_price = last_customer_price[0][0]
    else:
        last_customer_price = "Fist Sale"

    current_stock = get_latest_stock_qty(item_code)
    return {'item_price':last_customer_price,'current_stock':current_stock}

@frappe.whitelist()
def get_last_selling_price_of_supplier(item_code = '',customer = ''):

    last_customer_price = frappe.db.sql("""select rate,posting_date from `tabPurchase Invoice Item` sid inner join `tabPurchase Invoice` si on sid.parent= si.name where si.supplier = '{}' and sid.item_code = '{}' and si.docstatus != 2 order by si.posting_date DESC""".format(customer,item_code))
    if last_customer_price:
        last_customer_price = last_customer_price[0][0]
    else:
        last_customer_price = "Fist Sale"

    current_stock = get_latest_stock_qty(item_code)
    return {'item_price':last_customer_price,'current_stock':current_stock}

@frappe.whitelist()
def get_last_selling_prices_of_customer_delivery(item_code = '',customer = ''):

    last_customer_prices = frappe.db.sql("""select rate,posting_date from `tabDelivery Note Item` sid inner join `tabDelivery Note` si on sid.parent= si.name where si.customer = '{}' and sid.item_code = '{}' and si.docstatus != 2 order by si.posting_date DESC limit 5""".format(customer,item_code))
    if last_customer_prices:
        last_customer_price = last_customer_prices
    else:
        last_customer_price = [0,'']

    current_stock = get_latest_stock_qty(item_code)
    return {'item_price':last_customer_price,'current_stock':current_stock}

@frappe.whitelist()
def get_last_selling_prices_of_customer(item_code = '',customer = ''):

    last_purchase_price = frappe.db.sql("""select rate,posting_date,si.supplier from `tabPurchase Invoice Item` sid inner join `tabPurchase Invoice` si on sid.parent= si.name where sid.item_code = '{}' and si.docstatus != 2 order by si.posting_date DESC limit 5""".format(item_code))

    last_customer_prices = frappe.db.sql("""select rate,posting_date,si.customer from `tabSales Invoice Item` sid inner join `tabSales Invoice` si on sid.parent= si.name where si.customer != '{}' and sid.item_code = '{}' and si.docstatus != 2 order by si.posting_date DESC limit 3""".format(customer,item_code))
    last_customer_prices_customer = frappe.db.sql("""select rate,posting_date,si.customer from `tabSales Invoice Item` sid inner join `tabSales Invoice` si on sid.parent= si.name where si.customer = '{}' and sid.item_code = '{}' and si.docstatus != 2 order by si.posting_date DESC limit 3""".format(customer,item_code))
    last_selling = last_customer_prices_customer + last_customer_prices
    if last_selling:
        last_customer_price = last_selling
    else:
        last_customer_price = [0,'']

    current_stock = frappe.db.sql("""select warehouse,actual_qty from `tabBin` where item_code = '{}'""".format(item_code))
    return {'item_price':last_customer_price,'purchase_rate':last_purchase_price ,'stock_balance':current_stock}


