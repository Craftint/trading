# Copyright (c) 2013, Craft and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from trading.trading.report.fin_statement import (get_period_list, get_columns, get_data)

def execute(filters=None):
	period_list = get_period_list(filters.from_fiscal_year, filters.to_fiscal_year,
		filters.period_start_date, filters.period_end_date, filters.filter_based_on, filters.periodicity,
		company=filters.company)

	income = get_data(filters.company, "Income", "Credit", period_list, filters = filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True, ignore_accumulated_values_for_fy= True)

	expense = get_data(filters.company, "Expense", "Debit", period_list, filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True, ignore_accumulated_values_for_fy= True)

	net_profit_loss = get_net_profit_loss(income, expense, period_list, filters.company, filters.presentation_currency)

	data = []
	data.extend(income or [])
	data.extend(expense or [])

	sales = cost = sales_t = cost_t = total_gp = 0
	sales_dict = {}
	cost_dict = {}
	lab = ''

	if filters.periodicity == "Yearly":
		for inc_dict in income:
			if inc_dict:
				if inc_dict["account_name"]=="Sales":
					sales = inc_dict["total"]
					break
	
	else:
		for inc_dict in income:
			if inc_dict:
				if inc_dict["account_name"]=="Sales":
					inc = list(inc_dict.items())
					sales_dict = dict(list(inc_dict.items())[(list(inc_dict.keys()).index("account_name"))+1:len(inc_dict)-2])
					sales_t = inc_dict["total"]
					break
					

	if filters.periodicity == "Yearly":
		for exp_dict in expense:
			if exp_dict:
				if exp_dict["account_name"]=="Cost of Sale":
					cost = exp_dict["total"]
				if exp_dict["account_name"]=="Total Expense (Debit)":
					els = list(exp_dict.items())
					lab0 = els[-2]
					lab = lab0[0]
					break
	else:
		for exp_dict in expense:
			if exp_dict:
				if exp_dict["account_name"]=="Cost of Sale":
					exp = list(exp_dict.items())
					cost_dict = dict(list(exp_dict.items())[(list(exp_dict.keys()).index("currency"))+1:len(exp_dict)-1])
					cost_t = exp_dict["total"]
					break


	gp = flt((flt(sales,2)-flt(cost,2)),2)
	total_gp = flt((sales_t - cost_t),2)


	gp_dict = {}

	for k,v in sales_dict.items():
		gp_dict[k]= flt((v - cost_dict[k]),2)

		
	if filters.periodicity == "Yearly":
		data.append({
			'account_name': 'Gross Profit', 
			'account': 'Gross Profit', 
			'currency': 'AED', 
			lab: gp, 
			'total': gp},
			)
	else:
		gp_dict.update({
			'account_name': 'Gross Profit', 
			'account': 'Gross Profit', 
			'currency': 'AED', 
			'total': total_gp
			},
			)
		data.append(gp_dict)

	if net_profit_loss:
		data.append(net_profit_loss)

	columns = get_columns(filters.periodicity, period_list, filters.accumulated_values, filters.company)

	chart = get_chart_data(filters, columns, income, expense, net_profit_loss)

	return columns, data, None, chart

def get_net_profit_loss(income, expense, period_list, company, currency=None, consolidated=False):
	total = 0
	net_profit_loss = {
		"account_name": "'" + _("Profit for the year") + "'",
		"account": "'" + _("Profit for the year") + "'",
		"warn_if_negative": True,
		"currency": currency or frappe.get_cached_value('Company',  company,  "default_currency")
	}

	has_value = False

	for period in period_list:
		key = period if consolidated else period.key
		total_income = flt(income[-2][key], 3) if income else 0
		total_expense = flt(expense[-2][key], 3) if expense else 0

		net_profit_loss[key] = total_income - total_expense

		if net_profit_loss[key]:
			has_value=True

		total += flt(net_profit_loss[key])
		net_profit_loss["total"] = total

	if has_value:
		return net_profit_loss

def get_chart_data(filters, columns, income, expense, net_profit_loss):
	labels = [d.get("label") for d in columns[2:]]

	income_data, expense_data, net_profit = [], [], []

	for p in columns[2:]:
		if income:
			income_data.append(income[-2].get(p.get("fieldname")))
		if expense:
			expense_data.append(expense[-2].get(p.get("fieldname")))
		if net_profit_loss:
			net_profit.append(net_profit_loss.get(p.get("fieldname")))

	datasets = []
	if income_data:
		datasets.append({'name': _('Income'), 'values': income_data})
	if expense_data:
		datasets.append({'name': _('Expense'), 'values': expense_data})
	if net_profit:
		datasets.append({'name': _('Net Profit/Loss'), 'values': net_profit})

	chart = {
		"data": {
			'labels': labels,
			'datasets': datasets
		}
	}

	if not filters.accumulated_values:
		chart["type"] = "bar"
	else:
		chart["type"] = "line"

	chart["fieldtype"] = "Currency"

	return chart