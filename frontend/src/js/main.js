require(["jquery","jquery.address","underscore"], 
	function() {

        var addToRenderList = function(e,state){
     

            var model_id = e.currentTarget.id;
            var renderlist = state['toRender'];
            if (renderlist === undefined){
                renderlist = [];
            }
            if (!(_.include(renderlist,model_id))){
               renderlist.push(model_id);             
               $('#renderlist').append("<div>" + model_id + "</div>");
               state['toRender'] = renderlist;
               $.address.jsonhash(state);
               $.address.update();
            }
        };
        
		var showfunc = function(params,state){
		    var by = state["by"];
		    var qval = {};
		    qval[by] = state["val"];
			var params = {"query":JSON.stringify(qval)};

			$.address.path("/show");
			$.address.jsonhash(state);
			$.address.update();
			$.ajax({
				url: "http://localhost:9999/models",
				dataType: 'jsonp',
				data:params,
				traditional:true,
				success: function(data) {
					$("#content div,span").remove();
					var path, thing, model_id;

					$.each(data,function(i,v){
						
						path = v['filepath']
						model_id = v['id']
		
						thing = $('<span id=' + model_id + '><img src="http://dicarlocox-3dmodels-images.s3.amazonaws.com/' + path + '" height="200px"/>' + model_id + '</span>')
						thing.click(function(e){ 
						    addToRenderList(e,state);
						});
						$("#content").append(thing);


		
					});
					
				}
			});	        
		
		};
	
	    var choosefunc = function(params,state){
	    
	        var by = state["by"];
	        if (by === undefined){
	            by = "keywords";
	            state["by"] = by;
	        }
	        
	        $.address.jsonhash(state);
	        $.address.update();
			$.ajax({
				url: "http://localhost:9999/models",
				dataType: 'jsonp',
				data: {action:"distinct",field:by},
				traditional:true,
				success: function(data) {
					$("#content div,span").remove();
					var thing;
					$.each(data,function(ind,val){
						thing = $('<div class="choose_item">' + val + "</div>");
						thing.click(function(){
						    state["val"] = val;
							showfunc(params,state);
						});
						
						$("#content").append(thing);
				
						
					});
					
	
				}
			});
        };

		$.address.init(function(e) {
		    $.address.autoUpdate(false);

		}).externalChange(function(e) {
			var state = $.address.jsonhash();
			state = state || {};
			var params = $.address.parameters();
	        var path = e.path;
	        
		    $("#chooseByTag").unbind();
		    $("#chooseByTag").click(function(){
		        state["by"] = "keywords";
		        $.address.path("/choose");
		        delete state["val"];
		        choosefunc(params,state)
		    });

		    $("#chooseByName").unbind();
		    $("#chooseByName").click(function(){
		        state["by"] = "name";
		        $.address.path("/choose");
		        delete state["val"];
		        choosefunc(params,state)
		    });

            $('#renderlist div').remove();
	        var renderlist = state['toRender'];
	        if (renderlist !== undefined){
	            $.each(renderlist,function(i,v){
	                $('#renderlist').append("<div>" + v + "</div>");
	            });
	        }
	 
	        if ((path === "/choose") || (path === "/")) {
	            if (path === "/"){
    	            $.address.path("/choose");
    	        }
	            choosefunc(params,state);
	        } else if (path === "/show") {
	            showfunc(params,state);
	        }
	        
			
	  });	   
			
});

