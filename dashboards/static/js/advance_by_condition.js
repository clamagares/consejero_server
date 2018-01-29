

var advance_topics_3 = [];
var condition_names = [];
var datasets_advance_by_conditions = [];

function showObjectjQuery5(obj) {
	$.each(obj, function(k, v) {
		condition_names.push(k);
		$.each(obj[k], function(k1, v1) {
			if (!arrayContains(k1,advance_topics_3)) {
				advance_topics_3.push(k1);
			}
		});
	});
}
showObjectjQuery5(advance_by_condition);




function organizeAdvances3(){

			
	advance_topics_3.forEach(function (topic_name, i) {
		var topic_for_push;
		var data_pack = [];
		condition_names.forEach(function (condition_name, i) {
			
			if (advance_by_condition[condition_name][topic_name]) {
				data_pack.push(advance_by_condition[condition_name][topic_name]);
			}else{
				data_pack.push(0);
			}
				
		});
		
		datasets_advance_by_conditions.push({label:topic_name, data: data_pack,backgroundColor:"#"+(Math.random()*0xFFFFFF<<0).toString(16)});
		
	});

}





organizeAdvances3();




var bar_ctx = document.getElementById('advance_by_condition');
var bar_chart = new Chart(bar_ctx, {
    type: 'bar',
    data: {
        labels: condition_names,
        datasets: datasets_advance_by_conditions
    },
    options: {
     		animation: {
        	duration: 10,
        },
        scales: {
          xAxes: [{ 
          	stacked: true, 
            gridLines: { display: false },
            }],
          yAxes: [{ 
          	stacked: true, 
            
            }],
        }, // scales
        legend: {display: true}
    } // options
   }
);







function arrayContains(needle, arrhaystack)
{
    return (arrhaystack.indexOf(needle) > -1);
}
