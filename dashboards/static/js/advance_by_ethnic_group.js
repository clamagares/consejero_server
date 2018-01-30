

var advance_topics_2 = [];
var ethnic_group_names = [];
var datasets_advance_by_ethnic_group = [];

function showObjectjQuery4(obj) {
	$.each(obj, function(k, v) {
		ethnic_group_names.push(k);
		$.each(obj[k], function(k1, v1) {
			if (!arrayContains(k1,advance_topics_2)) {
				advance_topics_2.push(k1);
			}
		});
	});
}
showObjectjQuery4(advance_by_ethnic_group);




function organizeAdvances2(){


	advance_topics_2.forEach(function (topic_name, i) {
		var topic_for_push;
		var data_pack = [];
		ethnic_group_names.forEach(function (ethnic_name, i) {

			if (advance_by_ethnic_group[ethnic_name][topic_name]) {
				data_pack.push(advance_by_ethnic_group[ethnic_name][topic_name]);
			}else{
				data_pack.push(0);
			}

		});

		datasets_advance_by_ethnic_group.push({label:topic_name, data: data_pack,backgroundColor:"#"+(Math.random()*0xF0F0F0<<0).toString(16)});

	});

}





organizeAdvances2();




var bar_ctx = document.getElementById('advance_by_ethnic_group');
var bar_chart = new Chart(bar_ctx, {
    type: 'bar',
    data: {
        labels: ethnic_group_names,
        datasets: datasets_advance_by_ethnic_group
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
