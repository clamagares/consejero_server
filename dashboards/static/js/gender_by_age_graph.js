

var labels = [];
var genders_names = [];
var genders_ages = ['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80-84', '85-+'].reverse();


function showObjectjQuery2(obj) {
  $.each(obj, function(k1, v1) {
    genders_names.push(k1);
  });
}
showObjectjQuery2(gender_by_age);



function fillGraph(){
  var index = 0;
  genders_names.forEach(function (gender_name, i) {
    $("#gender_by_age_div").append("<canvas id="+gender_name+"   ></canvas>");
    var ages_for_graph = [];
    var backgounds= [];
    genders_ages.forEach(function (gender_age, i) {
      backgrounds.push("#"+(Math.random()*0xF0F0F0<<0).toString(16));
      if (gender_age in gender_by_age[gender_name]){
        ages_for_graph.push(gender_by_age[gender_name][gender_age]);
      }else{
        ages_for_graph.push(0);
      }
    });



    new Chart(document.getElementById(gender_name), {
      type: 'horizontalBar',
      data: {
        labels: genders_ages,
        datasets: [
        {
          backgroundColor: backgrounds,
          data: ages_for_graph
        }
        ]
      },
      options: {
        legend: { display: false },
        title: {
          display: true,
          text: 'Edades por género '+gender_name
        }
      }
    });


  });


}

fillGraph();
