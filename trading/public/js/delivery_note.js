

frappe.ui.form.on("Delivery Note", {

	"after_save": function(frm) {
		if (frm.doc.manual) {
			if((frm.doc.manual_naming_series != frm.doc.name) && (!frm.doc.__islocal)) {				
				frappe.call({
					method: "trading.events.delivery_note.change_autoname_after_save",
					args:{
						"name":frm.doc.name,
						"manual_naming_series":frm.doc.manual_naming_series
					},
					callback: function(r) {
						frappe.set_route("Form", "Delivery Note", frm.doc.manual_naming_series);
					}
				});
			}			
		}		
	}
});

frappe.ui.form.on('Delivery Note Item', {
        item_code:function(frm,cdt,cdn){
     		var d = locals[cdt][cdn]
               frm.set_value( "item_code", d.item_code);
               frm.set_value( "item_name", d.item_name);
	

		console.log(d.item_code)
		frappe.call({
			method: "trading.trading.sales_invoice.get_last_selling_prices_of_customer",
			args:{
				item_code : d.item_code,
				customer : frm.doc.customer
			},
			callback: function(r) {
			
				/*debugger
				for(var i=0;i<r.message.item_price.length;i++){
					frappe.show_alert({message: __("Last Item Selling Price = {0}",[r.message.item_price[i][0]]), indicator: 'green'});
				}*/
			//	frappe.show_alert({message: __("Stock Balance = {0}",[r.message.current_stock]), indicator: 'green'});
                                
				//frm.set_value( “item_code”, d.item_code);
                	        var template = '<div style="width:100%"><div style="float:left;width:33%"><table class="table table-condensed table-hover table-bordered"><tbody><tr><th width=20%><b>Selling Price</b></th><th><b>Date</b></th><th width=50%><b>Customer</b></th></tr>{% for (var row in rows) { %}<tr>{% for (var col in rows[row]) { %}<td>{{ rows[row][col] }}</td>{% } %}</tr>{% } %}</tbody></table></div><div style="float:left;width:33%"><table class="table table-condensed table-hover table-bordered"><tbody><tr><th width=20%><b>Purchase Price</b></th><th><b>Date</b><th width=50%><b>Supplier</b></th></tr>{% for (var row in rows_purchase) { %}<tr>{% for (var col in rows_purchase[row]) { %}<td>{{ rows_purchase[row][col] }}</td>{% } %}</tr>{% } %}</tbody></table></div><div style="float:left;width:33%"><table class="table table-condensed table-hover table-bordered"><tbody><tr><th width=50%><b>Warehouse</b></th><th><b>Stock Qty</b></th></tr>{% for (var row in stock_balance) { %}<tr>{% for (var col in stock_balance[row]) { %}<td>{{ stock_balance[row][col] }}</td>{% } %}</tr>{% } %}</tbody></table></div></div>'


        		         frm.set_df_property('previous_transaction', 'options', frappe.render(template, {rows: r.message.item_price,rows_purchase:r.message.purchase_rate,stock_balance:r.message.stock_balance}));
                                   
        		frm.refresh_field('previous_transaction');
				//frm.set_value( “item_code”, d.item_code);
				//frm.refresh_field('item_code');
                                                                           

			
			}
		})
	},

})

