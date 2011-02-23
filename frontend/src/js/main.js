require(["jquery","jquery.address"], 
	function() {

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
						thing = $('<span><img src="http://dicarlocox-3dmodels-images.s3.amazonaws.com/' + path + '" height="200px"/>' + model_id + '</span>')
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
	            $.address.jsonhash(state);
	        }
	        
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
						thing = $("<div>" + val + "</div>");
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

