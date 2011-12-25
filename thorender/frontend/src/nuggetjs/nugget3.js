        /* nugget 1 code */
        $(document).ready(function(){
            var reducefunc = "function(doc,out){ \
                var planes={'MB27211': 1, 'MB27309': 1, 'MB27203': 1, 'MB26937': 1, 'MB27463': 1, 'MB27876': 1, 'MB28243': 1, 'MB27530': 1, 'MB29650': 1, 'MB27732': 1, 'MB28651': 1, 'MB28430': 1}; \
                if (doc.image.model_id in planes){ \
                    out.count1++; \
                    if (out.feature_average1 === 0){ \
                        out.feature_average1 = doc.feature; \
                        out.feature_var1 = []; \
                        for (ind=0;ind<doc.feature.length;ind++){ \
                            out.feature_var1.push(0); \
                        } \
                    } else {         \
                        for (ind=0;ind<doc.feature.length;ind++){ \
                            out.feature_average1[ind] = (1 - 1.0/out.count1)*out.feature_average1[ind] + (1.0/out.count1)*doc.feature[ind]; \
                            out.feature_var1[ind] = (out.count1-1)/out.count1*(out.feature_var1[ind] + (1/out.count1)*Math.pow(doc.feature[ind] - out.feature_average1[ind],2)); \
                        } \
                    } \
                }else{ \
                    out.count2++; \
                    if (out.feature_average2 === 0){ \
                        out.feature_average2 = doc.feature; \
                        out.feature_var2 = []; \
                        for (ind=0;ind<doc.feature.length;ind++){  \
                            out.feature_var2.push(0); \
                        } \
                    } else {        \
                        for (ind=0;ind<doc.feature.length;ind++){   \
                            out.feature_average2[ind] = (1 - 1.0/out.count2)*out.feature_average2[ind] + (1.0/out.count2)*doc.feature[ind]; \
                            out.feature_var2[ind] = (out.count2-1)/out.count2*(out.feature_var2[ind] + (1/out.count2)*Math.pow(doc.feature[ind] - out.feature_average2[ind],2)); \
                        } \
                    } \
                } \
            }"


            var w = 400;
            var h = 200;
		          
		    //var hash = '73a6f2263870c4a3cb44f0d4cdf3848f3de811ac';
            //var hash = 'fe3a9f56b840d0afbd50f3e383a944fd9302db4d';  
            var hash = '2883526ba801a25bdabacbf9bc4cd6ba6cf137d3';   // with percentile
        
            var reptiles = ['MB30418', 'MB31192', 'MB29694', 'adder', 'boa', 'bullfrog', 'chameleon', 'crocodile', 'gecko', 'iguana', 'leatherback', 'terapin', 'tortoise', 'treefrog', 'salamander'];
            //var reptiles = ['MB29694'];
            var planes = ['MB26937', 'MB27203', 'MB27211', 'MB27309', 'MB27463', 'MB27876', 'MB27732', 'MB27530', 'MB28430', 'MB29650', 'MB28651', 'MB28243'];
            //var planes = ['MB27530'];
            //var planes = ['MB27463'];

            var things = reptiles.concat(planes);
            var qval = {"__hash__":hash,"image.bg_id":"gray.tdl","image.ryz":{"$exists":false},"image.model_id":{"$in":things}};
            var nseg = 8;
            var rotnum = 5;
            var qvalr = {"__hash__":hash,"image.bg_id":"gray.tdl","image.ryz":{"$gt":2*Math.PI*rotnum/nseg - Math.PI,"$lt":2*Math.PI*(rotnum+1)/nseg-Math.PI},"image.model_id":{"$in":things}};
            var kval = ["model"];
            var ival = {"count1":0,"feature_average1":0,"feature_var1":0,"count2":0,"feature_average2":0,"feature_var2":0};
			var params = {"action":"group","keys":JSON.stringify(kval),"query":JSON.stringify(qval),
			              "initialize":JSON.stringify(ival),"reduce":reducefunc}; 
			var paramsr = {"action":"group","keys":JSON.stringify(kval),"query":JSON.stringify(qvalr),
			              "initialize":JSON.stringify(ival),"reduce":reducefunc}; 

            function plot_func(num,feats,vars,cts,stroke_color,x,y,g,line,vis){
                var data = feats[num];
           		var error = _.map(_.map(vars[num],Math.sqrt),function(e){return e/Math.sqrt(cts[num]);});

                var dataplus = _.map(_.zip(data,error),function(e){return e[0] + e[1];})
                var dataminus = _.map(_.zip(data,error),function(e){return e[0] - e[1];}) 
                g.append("svg:path").attr("d", line(data)).attr("style","stroke:" + stroke_color);
                
                g.selectAll("div").data(dataplus).enter().append("svg:line")
                .attr("x1",function(d,i){return x(i-.3);}).attr("x2",function(d,i){return x(i+.3);})
                .attr("y1",function(d,i){return -1*y(d);}).attr("y2",function(d,i){return -1*y(d);})

                g.selectAll("div").data(dataplus).enter().append("svg:line")
                .attr("x1",function(d,i){return x(i);}).attr("x2",function(d,i){return x(i);})
                .attr("y1",function(d,i){return -1*y(data[i]);}).attr("y2",function(d,i){return -1*y(d);})
                
                g.selectAll("div").data(dataminus).enter().append("svg:line")
                .attr("x1",function(d,i){return x(i-.3);}).attr("x2",function(d,i){return x(i+.3);})
                .attr("y1",function(d,i){return -1*y(d);}).attr("y2",function(d,i){return -1*y(d);})

                g.selectAll("div").data(dataminus).enter().append("svg:line")
                .attr("x1",function(d,i){return x(i);}).attr("x2",function(d,i){return x(i);})
                .attr("y1",function(d,i){return -1*y(data[i]);}).attr("y2",function(d,i){return -1*y(d);})                    
                
                g.append("svg:line").attr("x1", x(0)).attr("y1", -1 * y(0))
                .attr("x2", x(w)).attr("y2", -1 * y(0))
                
                g.append("svg:line").attr("x1", x(0)).attr("y1", -1 * y(0))
                .attr("x2", x(0)).attr("y2", -1 * y(d3.max(data)))
   
                g.selectAll(".xLabel").data(x.ticks(5)).enter().append("svg:text")
                .attr("class", "xLabel").text(String).attr("x", function(d) { return x(d) })
                .attr("y", -3).attr("text-anchor", "middle").attr("dx",8)
                
                var yticks = _.map(y.ticks(4),function(elt){return elt.toFixed(2);})
                g.selectAll(".yLabel").data(yticks).enter().append("svg:text")
                .attr("class", "yLabel").text(String).attr("x", 0).attr("y", function(d) { return -1 * y(d) })
                .attr("text-anchor", "right").attr("dy", 4).attr("dx",-8)
                
                g.selectAll(".xTicks").data(x.ticks(5)).enter().append("svg:line")
                .attr("class", "xTicks").attr("x1", function(d) { return x(d); })
                .attr("y1", -1 * y(0)).attr("x2", function(d) { return x(d); }).attr("y2", -1 * y(-0.3))

                g.selectAll(".yTicks").data(y.ticks(4)).enter().append("svg:line")
                .attr("class", "yTicks").attr("y1", function(d) { return -1 * y(d); })
                .attr("x1", x(-0.3)).attr("y2", function(d) { return -1 * y(d); }).attr("x2", x(0))                    
            }      
    
            function do_plot(features1,variances1,counts1,features2,variances2,counts2,num,vis,plotonly){
                var data1 = features1[num];
                var data2 = features2[num];
                var margin = 20;
                //var y = d3.scale.linear().domain([0, Math.max(d3.max(data1),d3.max(data2))]).range([0 + margin, h - margin]);
                var x = d3.scale.linear().domain([0, Math.max(data1.length,data2.length)]).range([0 + margin, w - margin]);
                var y = d3.scale.linear().domain([0,.2]).range([0 + margin, h - margin]);                    
                                     
                                     
                var g = vis.append("svg:g").attr("transform", "translate(0, 200)").attr("class","thing");
                
                var line = d3.svg.line().x(function(d,i) { return x(i); }).y(function(d) { return -1 * y(d); })
                
                if (plotonly === 1){
                    plot_func(num,features1,variances1,counts1,"blue",x,y,g,line,vis);
                } else if (plotonly === 2){
                    plot_func(num,features2,variances2,counts2,"red",x,y,g,line,vis);
                } else {
                    plot_func(num,features1,variances1,counts1,"blue",x,y,g,line,vis);
                    plot_func(num,features2,variances2,counts2,"red",x,y,g,line,vis);
                }
            }
             
            $.ajax({
                url: "http://50.19.109.25:9999/db/thor/features.files",
                dataType: 'jsonp',
                data:params,
                traditional:true,
                success: function(result){

                    var plot_num,features1,variances1,counts1,features2,variances2,counts2;
                    
                    features1 = _.pluck(result,"feature_average1");
                    variances1 = _.pluck(result,"feature_var1")
                    counts1 = _.pluck(result,"count1")
                    features2 = _.pluck(result,"feature_average2");
                    variances2 = _.pluck(result,"feature_var2")
                    counts2 = _.pluck(result,"count2")
                    models = _.pluck(result,"model")
                    
                    var vis = d3.select("#box1").append("svg:svg").attr('id',"plot").attr("width", w).attr("height", h).attr('style','padding-left:100px;padding-top:100px')
                    
                    $('#plot').click(function(){
                        plot_num = (plot_num + 1 ) % result.length;
                        $('#plot .thing').remove();
                        console.log("plotting model", plot_num,models[plot_num]['layers'][1]['filter']['ker_shape'],models[plot_num]['layers'][1]['activ']['min_out']);
                        do_plot(features1,variances1,counts1,features2,variances2,counts2,plot_num,vis);

                    });

                    plot_num = 0;
                    console.log("plotting model", plot_num,models[plot_num]['layers'][1]['filter']['ker_shape'],models[plot_num]['layers'][1]['activ']['min_out']);
                    do_plot(features1,variances1,counts1,features2,variances2,counts2,plot_num,vis);
    
                    
                   }	 
                })
                
            
            function sucfunc(result,vis,plot_num,plotonly){
                    var features1,variances1,counts1,features2,variances2,counts2;
                    features1 = _.pluck(result,"feature_average1");
                    variances1 = _.pluck(result,"feature_var1")
                    counts1 = _.pluck(result,"count1")
                    features2 = _.pluck(result,"feature_average2");
                    variances2 = _.pluck(result,"feature_var2")
                    counts2 = _.pluck(result,"count2")
                    do_plot(features1,variances1,counts1,features2,variances2,counts2,plot_num,vis,plotonly);
            };
               
            var F_CACHE = {};
            $.ajax({
                url: "http://50.19.109.25:9999/db/thor/features.files",
                dataType: 'jsonp',
                data:paramsr,
                traditional:true,
                success: function(result){
                    var vis = d3.select("#box2").append("svg:svg").attr('id',"plot2").attr("width", w).attr("height", h).attr('style','padding-left:100px;padding-top:100px')
                    plot_num = 0;
                    sucfunc(result,vis,plot_num)
                    F_CACHE[rotnum] = result;
                    
                    $('#plot2').click(function(){
                        rotnum = (rotnum + 1) % nseg;
                        console.log('rotnum',rotnum,F_CACHE)
                        if (!(rotnum in F_CACHE)){
                            qvalr["image.ryz"] = {"$gt":2*Math.PI*rotnum/nseg-Math.PI,"$lt":2*Math.PI*(rotnum+1)/nseg-Math.PI};
                            paramsr["query"] = JSON.stringify(qvalr);
                            $.ajax({
                                url:"http://50.19.109.25:9999/db/thor/features.files",
                                dataType: 'jsonp',
                                data:paramsr,
                                traditional:true,                        
                                success: function(res){
                                   $('#plot2 .thing').remove();
                                   console.log("plotting rotation", rotnum);
                                   F_CACHE[rotnum] = res;
                                   sucfunc(res,vis,plot_num);
                                }
                            }); 
                        } else {
                            $('#plot2 .thing').remove();
                            sucfunc(F_CACHE[rotnum],vis,plot_num);
                        }
                    });
                                        
                   }	 
                });                
        });
            
    




