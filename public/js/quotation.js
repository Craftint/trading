
frappe.ui.form.on('Quotation Item', {
        item_code:function(frm,cdt,cdn){
     		var d = locals[cdt][cdn]
	        frm.set_value( "item_code", d.item_code);
               frm.set_value( "item_name", d.item_name);

		frappe.call({
			method: "trading.trading.sales_invoice.get_last_selling_prices_of_customer",
			args:{
				item_code : d.item_code,
				customer : frm.doc.customer
			},
			callback: function(r) {
                               
				//frappe.show_alert({message: __("Last Item Selling Price = {0}",[r.message.item_price]), indicator: 'green'});
				//frappe.show_alert({message: __("Stock Balance = {0}",[r.message.current_stock]), indicator: 'green'});

				 var template = '<div style="width:100%"><div style="float:left;width:33%"><table class="table table-condensed table-hover table-bordered"><tbody><tr><th width=20%><b>Selling Price</b></th><th><b>Date</b></th><th width=50%><b>Customer</b></th></tr>{% for (var row in rows) { %}<tr>{% for (var col in rows[row]) { %}<td>{{ rows[row][col] }}</td>{% } %}</tr>{% } %}</tbody></table></div><div style="float:left;width:33%"><table class="table table-condensed table-hover table-bordered"><tbody><tr><th width=20%><b>Purchase Price</b></th><th><b>Date</b><th width=50%><b>Supplier</b></th></tr>{% for (var row in rows_purchase) { %}<tr>{% for (var col in rows_purchase[row]) { %}<td>{{ rows_purchase[row][col] }}</td>{% } %}</tr>{% } %}</tbody></table></div><div style="float:left;width:33%"><table class="table table-condensed table-hover table-bordered"><tbody><tr><th width=50%><b>Warehouse</b></th><th><b>Stock Qty</b></th></tr>{% for (var row in stock_balance) { %}<tr>{% for (var col in stock_balance[row]) { %}<td>{{ stock_balance[row][col] }}</td>{% } %}</tr>{% } %}</tbody></table></div></div>'

				//var template = '<div class="row"><div class="column"><table class="table table-condensed table-hover table-bordered"><tbody><tr><th width=50%><b>Selling Price</b></th><th><b>Date</b></th></tr>{% for (var row in stock_balance) { %}<tr>{% for (var col in rows[row]) { %}<td>{{ rows[row][col] }}</td>{% } %}</tr>{% } %}</tbody></table></div>'

                                frm.set_df_property('previous_transaction', 'options', frappe.render(template, {rows: r.message.item_price,rows_purchase:r.message.purchase_rate,stock_balance:r.message.stock_balance}));
				
                                frm.refresh_field('previous_transaction');

			}
		})
	},
})

