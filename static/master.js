var ctx = document.getElementById('barchart').getContext('2d');
var data = document.querySelector(".hidden-data").textContent
var options = ""
var yaxisButtons = document.querySelectorAll(".y-axis-buttons")
var myChart=null
yaxisButtons.forEach((button)=>{
    button.addEventListener("click",function(){
        options=this.textContent
        if(myChart!=null){
            myChart.destroy()
            myChart = createChart(options)
        }else{
            myChart = createChart(options)
        }
    });
});
console.log(data)
data = JSON.parse(data)
console.log(data)
const to_show = data

var intensities = data.map(function (entry) {
    return entry.intensity;
});
var relevances = data.map(function (entry) {
    return entry.relevance;
});
var likelihood_values = data.map(function (entry) {
    return entry.likelihood;
});
var labels = data.map(function (entry) {
    return entry.title;
});
myChart = createChart("")

function createChart(options){
    chosen_label=""
    chosen_data=null
    if(options=="Likelihood"){
        chosen_label="Likelihood"
        chosen_data=likelihood_values
    }
    else if(options=="Relevance"){
        chosen_label="Relevance"
        chosen_data=relevances
    }else{
        chosen_label="Intensity"
        chosen_data=intensities
    }
     const myChart = new Chart(ctx, {
     type: 'bar',
     data: {
       labels: labels,
       datasets: [{
               label: chosen_label,
                data: chosen_data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
      },
     options: {
       scales: {
         x: {
           display: false,
         },
         y:{
            title: {
                display: true,
                text: chosen_label
        }
         }
       },
       plugins: {
         legend: {
           display: false,
         },
         tooltip: {
           callbacks: {
             title: (tooltipItems) => {
               const index = tooltipItems[0].dataIndex;
               return labels[index];
             }
           }
         }
       }
     }
   });
   return myChart
}
