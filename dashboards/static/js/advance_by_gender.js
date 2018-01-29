

var genders_names_advance = [];
var datasets_advance_by_gender = [];
var advance_topics = [];

function showObjectjQuery3(obj) {
	$.each(obj, function(k, v) {
		genders_names_advance.push(k);
	});
}
showObjectjQuery3(gender_by_advance);

function organizeAdvances(){

	genders_names_advance.forEach(function (gender_name, i) {
		$.each(gender_by_advance[gender_name], function(k, v) {
			if (!arrayContains(k,advance_topics)) {
				advance_topics.push(k);
			}
		});
	});
			
	advance_topics.forEach(function (topic_name, i) {
		var topic_for_push;
		var data_pack = [];
		genders_names_advance.forEach(function (gender_name, i) {
			
			if (gender_by_advance[gender_name][topic_name]) {
				data_pack.push(gender_by_advance[gender_name][topic_name]);
			}else{
				data_pack.push(0);
			}
				
		});
		
		datasets_advance_by_gender.push({label:topic_name, data: data_pack,backgroundColor:"#"+(Math.random()*0xFFFFFF<<0).toString(16)});
		
	});

}





organizeAdvances();




var bar_ctx = document.getElementById('advance_by_gender');
var bar_chart = new Chart(bar_ctx, {
    type: 'bar',
    data: {
        labels: genders_names_advance,
        datasets: datasets_advance_by_gender
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
