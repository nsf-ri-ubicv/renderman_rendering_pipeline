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
            var reducefunc1 = "function(doc,out){ \
                var table={'MB31606': 1, 'MB28462': 1, 'MB28137': 1, 'MB28214': 1, 'MB30374': 1, 'MB28077': 1, 'MB30082': 1, 'MB27386': 1, 'MB30926': 1, 'MB28049': 1, 'MB28811': 1, 'MB30386': 1}; \
                if (doc.image.model_id in table){ \
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
            var hash = '3bccd08bc72671e67358064c75ad852b1b94c239';
            var hash1 = '2cdf50236e903ea79c56e2ddf848d8dee8cfd5c8';
        
            var faces = ['face0001', 'face0002', 'face0003', 'face0004', 'face0005', 'face0006', 'face0007', 'face0008', 'face1', 'face2', 'face3', 'face4', 'face5', 'face6', 'face7', 'face8'];
            var table = ['MB30374', 'MB30082', 'MB28811', 'MB27386', 'MB28462', 'MB28077', 'MB28049', 'MB30386', 'MB30926', 'MB28214', 'MB28137', 'MB31606'];
            var reptiles = ['MB30418', 'MB31192', 'MB29694', 'adder', 'boa', 'bullfrog', 'chameleon', 'crocodile', 'gecko', 'iguana', 'leatherback', 'terapin', 'tortoise', 'treefrog', 'salamander'];
            var planes = ['MB26937', 'MB27203', 'MB27211', 'MB27309', 'MB27463', 'MB27876', 'MB27732', 'MB27530', 'MB28430', 'MB29650', 'MB28651', 'MB28243'];
            var things = reptiles.concat(planes);
            var things1 = faces.concat(table); 
            var nseg = 20;
            var rotnum = 5;
            var rotnum1 = 5;
            var qval = {"__hash__":hash,"image.bg_id":"gray.tdl","image.ryz":{"$gt":2*Math.PI*rotnum/nseg - Math.PI,"$lt":2*Math.PI*(rotnum+1)/nseg-Math.PI},"image.model_id":{"$in":things}};
            var qval1 = {"__hash__":hash1,"image.bg_id":"gray.tdl","image.ryz":{"$gt":2*Math.PI*rotnum1/nseg - Math.PI,"$lt":2*Math.PI*(rotnum1+1)/nseg-Math.PI},"image.model_id":{"$in":things1}};
            var kval = ["model"];
            var ival = {"count1":0,"feature_average1":0,"feature_var1":0,"count2":0,"feature_average2":0,"feature_var2":0};

			var params = {"action":"group","keys":JSON.stringify(kval),"query":JSON.stringify(qval),
			              "initialize":JSON.stringify(ival),"reduce":reducefunc};
			var params1 = {"action":"group","keys":JSON.stringify(kval),"query":JSON.stringify(qval1),
			              "initialize":JSON.stringify(ival),"reduce":reducefunc1};              

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
                var y = d3.scale.linear().domain([0,.15]).range([0 + margin, h - margin]);                    
                                     
                                     
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
             

            function sucfunc(result,vis,plot_num,plotonly){
                    
                    var features1,variances1,counts1,features2,variances2,counts2;
                    features1 = _.pluck(result,"feature_average1");
                    variances1 = _.pluck(result,"feature_var1")
                    counts1 = _.pluck(result,"count1")
                    features2 = _.pluck(result,"feature_average2");
                    variances2 = _.pluck(result,"feature_var2")
                    counts2 = _.pluck(result,"count2")
                    console.log(features1)
                    do_plot(features1,variances1,counts1,features2,variances2,counts2,plot_num,vis,plotonly);
            };
               
            var F_CACHE = {};
            $.ajax({
                url: "http://50.19.109.25:9999/db/thor/features.files",
                dataType: 'jsonp',
                data:params,
                traditional:true,
                success: function(result){
                    var vis = d3.select("#box1").append("svg:svg").attr('id',"plot").attr("width", w).attr("height", h).attr('style','padding-left:100px;padding-top:100px')
                    plot_num = 22;
                    sucfunc(result,vis,plot_num)
                    F_CACHE[rotnum] = result;
                    $('#plot').click(function(){
                        rotnum = (rotnum + 1) % nseg;
                        console.log('rotnum',rotnum,1)
                        if (!(rotnum in F_CACHE)){
                            qval["image.ryz"] = {"$gt":2*Math.PI*rotnum/nseg-Math.PI,"$lt":2*Math.PI*(rotnum+1)/nseg-Math.PI};
                            params["query"] = JSON.stringify(qval);
                            $.ajax({
                                url:"http://50.19.109.25:9999/db/thor/features.files",
                                dataType: 'jsonp',
                                data:params,
                                traditional:true,                        
                                success: function(res){
                                   $('#plot .thing').remove();
                                   console.log("plotting rotation", rotnum);
                                   F_CACHE[rotnum] = res;
                                   sucfunc(res,vis,plot_num);
                                }
                            }); 
                        } else {
                            $('#plot .thing').remove();
                            sucfunc(F_CACHE[rotnum],vis,plot_num);
                        }
                    });
                                        
                   }	 
                });  

            var F_CACHE1 = {};
            $.ajax({
                url: "http://50.19.109.25:9999/db/thor/features.files",
                dataType: 'jsonp',
                data:params1,
                traditional:true,
                success: function(result){
                    var vis = d3.select("#box2").append("svg:svg").attr('id',"plot1").attr("width", w).attr("height", h).attr('style','padding-left:100px;padding-top:100px')
                    plot_num = 12;
                    sucfunc(result,vis,plot_num)
                    F_CACHE1[rotnum] = result;
                    
                    $('#plot1').click(function(){
                        rotnum1 = (rotnum1 + 1) % nseg;
                        console.log('rotnum1',rotnum1,1)
                        if (!(rotnum1 in F_CACHE1)){
                            qval1["image.ryz"] = {"$gt":2*Math.PI*rotnum1/nseg-Math.PI,"$lt":2*Math.PI*(rotnum1+1)/nseg-Math.PI};
                            params1["query"] = JSON.stringify(qval1);
                            $.ajax({
                                url:"http://50.19.109.25:9999/db/thor/features.files",
                                dataType: 'jsonp',
                                data:params1,
                                traditional:true,                        
                                success: function(res){
                                   $('#plot1 .thing').remove();
                                   console.log("plotting rotation", rotnum);
                                   F_CACHE1[rotnum1] = res;
                                   sucfunc(res,vis,plot_num);
                                }
                            }); 
                        } else {
                            $('#plot1 .thing').remove();
                            sucfunc(F_CACHE1[rotnum1],vis,plot_num);
                        }
                    });
                                        
                   }	 
                });  
                
               
  
        });
            
    




