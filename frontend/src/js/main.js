require(["jquery","jquery.address","underscore"], 
    
	function() {

        var renderlist = [];
        var addToRenderList = function(o){
     
            var model_id = o.id;
            var model_name = $(o).attr("name");

            if (!(_.include(renderlist,model_id))){
               renderlist.push(model_id);         
               var obj = $('<div class="selected_model_box" id="' + model_id + '"><div class="selected_model_id">' + model_id + '<span class="remover"> (remove)</span></div><div class="selected_model_name">' + model_name + '</div></div>');
               $('#renderlist').append(obj);
               obj.find(".remover").click(function(f){

                   obj.remove();
                   renderlist = _.without(renderlist,model_id);
               });
  
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

            $("#content div, #content span").remove(); 
		    if (by === "keywords"){
		        var choose_all = $("<div>Select All</div>");
		        choose_all.click(function(){
		            $('#content').find(".model_box").each(function(ind,o){
		               addToRenderList(o);  
		            });
		        });
		        $('#content').append(choose_all);
		    }
		    
			$.ajax({
				url: "http://localhost:9999/models",
				dataType: 'jsonp',
				data:params,
				traditional:true,
				success: function(data) {
					
					var path, thing, model_id,model_name;

					$.each(data,function(i,v){
						
						path = v['filepath'];
						model_id = v['id'];
						model_name = v['name'];
		
						thing = $('<div class="model_box" id="' + model_id + '" name="' + model_name + '"><div class="model_box_img"><img src="http://dicarlocox-3dmodels-images.s3.amazonaws.com/' + path + '" height="200px"/></div><div class="model_box_id">' + model_id + '</div><div class="model_box_name">' + model_name + '</div></span>')
						thing.click(function(e){ 
						    addToRenderList(e.currentTarget);
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
					$("#content div, #content span").remove();
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

            $("#render_it").unbind();
            $("#render_it").click(function(){
                var tX = $("#tX input").val();
                var tY = $("#tY input").val();
                var tZ = $("#tZ input").val();
                var rXY = $("#rXY input").val();
                var rXZ = $("#rXZ input").val();
                var rYZ = $("#rYZ input").val();
                var kenv = $("#kenv input").val();
                
                var renderliststring = JSON.stringify(renderlist);
                var paramstring = '&tx=' + tX + '&ty=' + tY + '&tz=' + tZ + '&rxy=' + rXY + '&rxz=' + rXZ + '&ryz=' + rYZ + '&kenv=' + kenv;
                
                              
                location.href = "http://localhost:9999/render?model_id=" + renderliststring + paramstring;

            });

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

