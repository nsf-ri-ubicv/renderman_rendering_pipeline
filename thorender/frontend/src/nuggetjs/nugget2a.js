        /* nugget 1 code */
        $(document).ready(function(){
            
            //var hash = 'e2cea1ed97916660defcdced4eacb6a674f5413d';   // all reptiles vs planes
            //var hash = '561ecc17188990ce63ad4c95bddb7199f2e413a4'; // gecko & box turtle more examples
            //var hash = '4ef76acd4ee4b9138e4ee9688a738c6cec141f88'; // geck and box turtel vs individual planes
            //var hash = 'ca5d2fb651c9461098afd0bb48f4ba45baa23661'; //lizard and leatherback vs individual planes
            //var hash = 'cfda7c95476a8b825c798ca8cb82d746c1395085'; // lizard vs all planes
            //var hash = 'af4ee0838ff90bd114c140930b3acdeb370bb146'; //reptiles vs planes drawing on more examples
            var hash = '59d6cbfeca5d00ccb3e9f7456ababcbf505644c4'; //reptiles vs planes with percentiles
            var hash = '833de2aff10bbe71cfec5af89b43e196895c65de';
            //var hash = '4aeb85163a6ffb4a2628cc8b9a3eab8279931ff8';
            
            var qval = {"__hash__":hash,"model.layers.1.activ.min_out":{"$lt":.5}}; 
            //var qval = {"__hash__":hash}; 
			var params = {"query":JSON.stringify(qval),"fields":JSON.stringify(["task.task_label","test_accuracy"])};

			var sortcol = "trans";
			var sortdir = 1;
			var dataView;
			var selectedRowIds = [];
	
			function HighlightFormatter(row, cell, value, columnDef, dataContext) {
			    var fw,fs,color;
			    value = (cell <= 1 ? value : value.toFixed(2) + '%');
			    fw = "normal";
			    fs = "normal";
			    
			    color = "black";
					
				return "<span style='color:" + color + ";font-style:" + fs + ";font-weight:" + fw + "'>" + value + "</span>";
			}	
	
			function comparer(a,b) {
				var x = a[sortcol], y = b[sortcol];
				return (x == y ? 0 : (x > y ? 1 : -1));
			}

			$.ajax({
				url: "http://50.19.109.25:9999/db/thor/performance",
				dataType: 'jsonp',
				data:params,
				traditional:true,
				success: function(data){
				   var tasks = _.uniq(_.map(data,function(e){return e['task']['task_label'].split(' ')[0];})); 
                   var cdata = {};
                   $.each(tasks,function(ind,h){
                       cdata[h] = {'trans mixed':[],'trans':[],'inrot':[]};
                   });
                   $.each(data,function(ind,elt){
                       var b = elt['task']['task_label'].split(' ');
                       var c = b.slice(1).join(' ');
                       cdata[b[0]][c].push(elt["test_accuracy"]);
                   });
                   var sar;
                   var statfunc = max;
                   console.log(data.length)
                   var data_array = _.map(tasks,function(elt){                   
					   return {cat1 : elt.split('/')[0],
					           cat2 : elt.split('/')[1],
						       trans : statfunc(cdata[elt]['trans']),
						       inrot : statfunc(cdata[elt]['inrot']),
						       mixed : statfunc(cdata[elt]['trans mixed']),
						       rot_delta : statfunc(cdata[elt]['trans']) - statfunc(cdata[elt]['inrot']),
						       mix_delta : statfunc(cdata[elt]['trans']) - statfunc(cdata[elt]['trans mixed']),
						       id : elt}
					});       
                   var grid;
				   var columns = [
						{id:"cat1", name:"Category1", field:"cat1",formatter:HighlightFormatter,width:75,sortable:true},
						{id:"cat2", name:"Category2", field:"cat2",formatter:HighlightFormatter,width:100,sortable:true},
						{id:"trans", name:"Trans", field:"trans",formatter:HighlightFormatter,sortable:true,width:60},
						{id:"inrot", name:"Inrot", field:"inrot",formatter:HighlightFormatter,sortable:true,width:60},
						{id:"mixed", name:"Mixed", field:"mixed",formatter:HighlightFormatter,sortable:true,width:60},
						{id:"rot_delta", name:"T - I", field:"rot_delta",formatter:HighlightFormatter,sortable:true,width:60},
						{id:"mix_delta", name:"T - M", field:"mix_delta",formatter:HighlightFormatter,sortable:true,width:60},
				   ];
				   var options = {
				        rowHeight : 18, 
						enableCellNavigation: false,
						enableColumnReorder: false
				   };
				   $(function() {	
				        dataView = new Slick.Data.DataView(); 
				        grid = new Slick.Grid($("#grid2"), dataView.rows, columns, options);
						grid.onSort = function(sortCol, sortAsc) {
						    console.log('sorting')
							sortdir = sortAsc ? 1 : -1;
							sortcol = sortCol.field;
			
							dataView.sort(comparer,sortAsc);

						};
			

						// wire up model events to drive the grid
						dataView.onRowCountChanged.subscribe(function(args) {
							grid.updateRowCount();
							grid.render();
						});
			
						dataView.onRowsChanged.subscribe(function(rows) {
							grid.removeRows(rows);
							grid.render();
			
							if (selectedRowIds.length > 0)
							{
								// since how the original data maps onto rows has changed,
								// the selected rows in the grid need to be updated
								var selRows = [];
								for (var i = 0; i < selectedRowIds.length; i++)
								{
									var idx = dataView.getRowById(selectedRowIds[i]);
									if (idx != undefined)
										selRows.push(idx);
								}
			
								grid.setSelectedRows(selRows);
							}
						});
		
						dataView.beginUpdate();
			            dataView.setItems(data_array);
			            dataView.endUpdate();	
				   })	 
				}
			});	     

        });
