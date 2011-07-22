
var min = _.min;

var max = _.max;

function sum(arr){
	return _.reduce(arr, function(memo, num){ return memo + num; }, 0);
};

function mean(arr){
	return sum(arr)/arr.length;
};

function variance(arr){
	var L = arr.length;
	var m = mean(arr);
	var ms = mean(_.map(arr,function(num){return num*num;}));
	return ms - m*m;
};

function std(arr){
	return Math.sqrt(variance(arr));
};

function scoreatpercentile(arr,percentile){
	var sorted = _.sortBy(arr,function(num){return num;})

	if (arr.length == 1) return arr[0];
	
	var ntileRank = ((percentile/100) * (arr.length - 1)) + 1;
	var integralRank = Math.floor(ntileRank);
	var fractionalRank = ntileRank - integralRank;
	var lowerValue = arr[integralRank-1];
	var upperValue = arr[integralRank];
	return (fractionalRank * (upperValue - lowerValue)) + lowerValue;
	
};

function product(arr_list){
    if (arr_list.length == 1){
        return _.map(arr_list[0],function(elt){return [elt];})
    } else{
        var subproduct = product(arr_list.slice(1));
        var productlist = _.map(arr_list[0],function(elt){return _.map(subproduct,function(selt){return [elt].concat(selt);});});
        return _.reduce(productlist,function(mem,elt){return mem.concat(elt)},[]);
        
    }
};