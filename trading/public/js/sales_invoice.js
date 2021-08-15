frappe.ui.form.on('Sales Invoice', {
	
	onload:function(frm){
		if(frm.doc.__islocal == 1){
			frm.set_value("update_stock",1)
		}
	},
	refresh:function(frm){
	    if(frm.doc.__islocal == 1){
	    	if(frm.doc.delivery_note){
			frm.set_value("update_stock",0)
		}
	    	else{
			frm.set_value("update_stock",1)
	   	}
            }
		
		if(!frm.doc.__islocal && (frm.doc.docstatus==0)){
			var global_frm = frm;
			frappe.call({
				method: "trading.events.sales_invoice.check_if_manual_and_manual_series_exist",
				
				args:{
					"name":frm.doc.name
				},
				callback: function(r) {
					let is_empty = jQuery.isEmptyObject(r.message);					
					if(!is_empty){
						setTimeout(function(){
							frm.set_value('manual', r.message[0].manual);
							frm.set_value('manual_naming_series', r.message[0].manual_naming_series);
							frm.refresh_fields(['manual', 'manual_naming_series']); 
						}, 1000);						
					}
				}
			});
		}		
	},
	setup:function(frm)
	{
		frm.set_indicator_formatter('item_code',
			function(doc) {
				return (doc.docstatus==1 || doc.qty<=doc.actual_qty) ? "green" : "orange"
			})
	},
	after_save:function(frm) {
		if (frm.doc.manual) {
			if((frm.doc.manual_naming_series != frm.doc.name) && (!frm.doc.__islocal)) {				
				frappe.call({
					method: "trading.events.sales_invoice.change_autoname_and_remarks_after_save",
					
					args:{
						"name":frm.doc.name,
						"manual_naming_series":frm.doc.manual_naming_series
					},
					callback: function(r) {
						frappe.set_route("Form", "Sales Invoice", frm.doc.manual_naming_series);
					}
				});
			}			
		}
	},
	// customer:function(frm){


	// 	frm.trigger('sales_person')
	// 	if(frm.doc.sales_person){
	// 		frm.doc.sales_team = []
	// 		var row = frm.add_child("sales_team");

	// 		row.sales_person = frm.doc.sales_person
	// 		row.allocated_percentage = 100
	// 		row.commission_rate = 1
	// 		row.allocated_amount = frm.doc.net_total
	// 		frm.refresh_field("sales_team")

	// 	}
	// },
	// sales_person:function(frm){

    //             if(frm.doc.sales_person){
    //                     frm.doc.sales_team = []
    //                     var row = frm.add_child("sales_team");

    //                     row.sales_person = frm.doc.sales_person
    //                     row.allocated_percentage = 100
	// 		row.commission_rate = 1
    //                     row.allocated_amount = frm.doc.net_total
    //                     frm.refresh_field("sales_team")

    //             }
    //     }

})

frappe.ui.form.on('Sales Invoice Item', {
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
	history:function(frm,cdt,cdn){
		var d = locals[cdt][cdn]
	        frappe.set_route('query-report', 'Item-wise Sales Register', {customer: frm.doc.customer});
		
	}

})

