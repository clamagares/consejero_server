

    var labels = [];
    var gender_percentage = [];
    var backgrounds = [];
    var hovers_backgounds = [];
    function showObjectjQuery(obj) {
      $.each(obj, function(k, v) {
        labels.push(k + " " + v);
        gender_percentage.push(v);
        backgrounds.push("#"+(Math.random()*0xF0F0F0<<0).toString(16));
        hovers_backgounds.push("#"+(Math.random()*0xF0F0F0<<0).toString(16));
      });
    }
showObjectjQuery(genders);

    var randomScalingFactor = function() {
      return Math.round(Math.random() * 100);
    };
    var randomColorFactor = function() {
      return Math.round(Math.random() * 255);
    };
    var randomColor = function(opacity) {

      return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',' + (opacity || '.3') + ')';
    };



    var config = {
      type: 'pie',
      data: {
        datasets: [{
          data: gender_percentage,
          label: 'Géneros',
          backgroundColor: backgrounds,
        }],
        labels: labels,

      },
      options: {
        responsive: true,
        legend: {
          position: 'bottom',
        },
        title: {
          display: false,
          text: 'Chart.js Doughnut Chart'
        },
        animation: {
          animateScale: true,
          animateRotate: true
        },
        tooltips: {
          callbacks: {
            label: function(tooltipItem, data) {
             var dataset = data.datasets[tooltipItem.datasetIndex];
             var total = dataset.data.reduce(function(previousValue, currentValue, currentIndex, array) {
              return previousValue + currentValue;
            });
             var currentValue = dataset.data[tooltipItem.index];
             var precentage = Math.floor(((currentValue/total) * 100)+0.5);
             return precentage + "%";
           }
         }
       }
     }
   };


   var ctx = document.getElementById("pie_gender").getContext("2d");
   window.myDoughnut = new Chart(ctx, config); {

   }
