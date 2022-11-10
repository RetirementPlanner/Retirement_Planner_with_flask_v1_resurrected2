//This function generates a Chartsjs chart.
//Inputs
//          1) chartType (as per ChartJS specs - e.g. 'line', 'bar'),
//          2) htmlID (id of HTML Canvas item that needs to go ahead of running this function)
//         3) Stacked_status (Boolean)
//          4) labels (list of label values for x axis)
 //         5) legend (string - used in roll over)
//          6) values (list of values)
//
//Output - Script that can amend canvas with ID"myChart" placed above script
   //       E.g.     <canvas id="[htmlID]" width="800" height="400"></canvas>

//Global settings

var heightRatio = 1;

//-------------------------------------------------------------------------------
//1) ONE DATA SETS
function chartGenerator_1(chartType, html_ID, stacked_status, chartLabels,  chartLegend_1,  chartValues_1 ) {
// 1) define the chart data
         var chartData =
            {
                labels: chartLabels,
                datasets : [
                    {label: chartLegend_1, data : chartValues_1, borderColor: 'rgba(255, 99, 132, 0.2)', backgroundColor:  'rgba(255, 99, 132, 0.2)', fill: 'origin'}
                           ]
            }

// 2) get chart canvas
          var ctx = document.getElementById(html_ID);
          ctx.height=ctx.width*heightRatio;

// 3) create the chart using the chart canvas
        var myChart = new Chart(ctx, {
                                        type: chartType,
                                        data: chartData,
                                        options:{
                                            scales: {
                                                        y:{
                                                            stacked: stacked_status,
                                                            ticks:{
                                                                callback: function(value) {
                                                                    return value.toLocaleString('en-UK', {style:'currency', currency:'GBP', maximumFractionDigits:0});
                                                                                            }
                                                                    },
                                                             },
                                                        x:{
                                                            stacked: stacked_status,
                                                            ticks:{

                                                                    }
                                                             },
                                                     }
                                                 }
                                 });


    return(myChart);
}



//-----------------------------------------------------------
//2) TWO DATA SETS
function chartGenerator_2(chartType, html_ID, stacked_status, chartLabels,  chartLegend_1,  chartValues_1, chartLegend_2,  chartValues_2 ) {
// 1) define the chart data
         var chartData =
            {
                labels: chartLabels,
                datasets : [
                    {label: chartLegend_1, data : chartValues_1, borderColor: 'rgba(255, 99, 132, 0.2)', backgroundColor:  'rgba(255, 99, 132, 0.2)', fill: 'origin'},
                    {label: chartLegend_2, data : chartValues_2, borderColor: 'rgba(54, 162, 235, 0.2)',backgroundColor: 'rgba(54, 162, 235, 0.2)', fill: '-1'}
                           ]
            }

// 2) get chart canvas
          var ctx = document.getElementById(html_ID);
          ctx.height=ctx.width*heightRatio;

// 3) create the chart using the chart canvas
        var myChart = new Chart(ctx, {
                                        type: chartType,
                                        data: chartData,
                                        options:{
                                            scales: {
                                                        y:{
                                                            stacked: stacked_status,
                                                            ticks:{
                                                                callback: function(value) {
                                                                    return value.toLocaleString('en-UK', {style:'currency', currency:'GBP', maximumFractionDigits:0});
                                                                                            }
                                                                    },
                                                             },
                                                        x:{
                                                            stacked: stacked_status,
                                                            ticks:{

                                                                    }
                                                             },
                                                     }
                                                 }
                                 });


    return(myChart);
}


//----------------------------------------------------------
//3) THREE DATA SETS
function chartGenerator_3(chartType, html_ID, stacked_status, chartLabels,  chartLegend_1,  chartValues_1, chartLegend_2,  chartValues_2, chartLegend_3,  chartValues_3 ) {
// 1) define the chart data
         var chartData =
            {
                labels: chartLabels,
                datasets : [
                    {label: chartLegend_1, data : chartValues_1, borderColor: 'rgba(255, 99, 132, 0.2)', backgroundColor:  'rgba(255, 99, 132, 0.2)', fill: 'origin'},
                    {label: chartLegend_2, data : chartValues_2, borderColor: 'rgba(54, 162, 235, 0.2)',backgroundColor: 'rgba(54, 162, 235, 0.2)', fill: '-1'},
                    {label: chartLegend_3, data : chartValues_3, borderColor: 'rgba(191, 63, 178, 0.2)',backgroundColor: 'rgba(191, 63, 178, 0.2)', fill: '-1'}
                           ]
            }

// 2) get chart canvas
          var ctx = document.getElementById(html_ID);
          ctx.height=ctx.width*heightRatio;

// 3) create the chart using the chart canvas
        var myChart = new Chart(ctx, {
                                        type: chartType,
                                        data: chartData,
                                        options:{
                                            scales: {
                                                        y:{
                                                            stacked: stacked_status,
                                                            ticks:{
                                                                callback: function(value) {
                                                                    return value.toLocaleString('en-UK', {style:'currency', currency:'GBP', maximumFractionDigits:0});
                                                                                            }
                                                                    },
                                                             },
                                                        x:{
                                                            stacked: stacked_status,
                                                            ticks:{

                                                                    }
                                                             },
                                                     }
                                                 }
                                 });


    return(myChart);
}

//---------------------------------------------------------------------------
//4) FOUR DATA SETS
function chartGenerator_4(chartType, html_ID, stacked_status, chartLabels,  chartLegend_1,  chartValues_1, chartLegend_2,  chartValues_2, chartLegend_3,  chartValues_3, chartLegend_4,  chartValues_4 ) {
// 1) define the chart data
         var chartData =
            {
                labels: chartLabels,
                datasets : [
                    {label: chartLegend_1, data : chartValues_1, borderColor: 'rgba(255, 99, 132, 0.2)', backgroundColor:  'rgba(255, 99, 132, 0.2)', fill: 'origin'},
                    {label: chartLegend_2, data : chartValues_2, borderColor: 'rgba(54, 162, 235, 0.2)',backgroundColor: 'rgba(54, 162, 235, 0.2)', fill: '-1'},
                    {label: chartLegend_3, data : chartValues_3, borderColor: 'rgba(191, 63, 178, 0.2)',backgroundColor: 'rgba(191, 63, 178, 0.2)', fill: '-1'},
                    {label: chartLegend_4, data : chartValues_4, borderColor: 'rgba(191, 112, 63, 0.2)',backgroundColor: 'rgba(191, 112, 63, 0.2)', fill:'-1'}
                            ]
            }

// 2) get chart canvas
          var ctx = document.getElementById(html_ID);
          ctx.height=ctx.width*heightRatio;

// 3) create the chart using the chart canvas
        var myChart = new Chart(ctx, {
                                        type: chartType,
                                        data: chartData,
                                        options:{
                                            scales: {
                                                        y:{
                                                            stacked: stacked_status,
                                                            ticks:{
                                                                callback: function(value) {
                                                                    return value.toLocaleString('en-UK', {style:'currency', currency:'GBP', maximumFractionDigits:0});
                                                                                            }
                                                                    },
                                                             },
                                                        x:{
                                                            stacked: stacked_status,
                                                            ticks:{

                                                                    }
                                                             },
                                                     }
                                                 }
                                 });


    return(myChart);
}

//---------------------------------------------------------------------------
//5) Five DATA SETS
function chartGenerator_5(chartType, html_ID, stacked_status, chartLabels,  chartLegend_1,  chartValues_1, chartLegend_2,  chartValues_2, chartLegend_3,  chartValues_3, chartLegend_4,  chartValues_4, chartLegend_5,  chartValues_5 ) {
// 1) define the chart data
         var chartData =
            {
                labels: chartLabels,
                datasets : [
                    {label: chartLegend_1, data : chartValues_1, borderColor: 'rgba(255, 99, 132, 0.2)', backgroundColor:  'rgba(255, 99, 132, 0.2)', fill: 'origin'},
                    {label: chartLegend_2, data : chartValues_2, borderColor: 'rgba(54, 162, 235, 0.2)',backgroundColor: 'rgba(54, 162, 235, 0.2)', fill: '-1'},
                    {label: chartLegend_3, data : chartValues_3, borderColor: 'rgba(191, 63, 178, 0.2)',backgroundColor: 'rgba(191, 63, 178, 0.2)', fill: '-1'},
                    {label: chartLegend_4, data : chartValues_4, borderColor: 'rgba(191, 112, 63, 0.2)',backgroundColor: 'rgba(191, 112, 63, 0.2)', fill:'-1'},
                    {label: chartLegend_5, data : chartValues_5, borderColor: 'rgba(54, 112, 63, 0.2)',backgroundColor: 'rgba(54, 112, 63, 0.2)', fill:'-1'}
                            ]

            }

// 2) get chart canvas
          var ctx = document.getElementById(html_ID);
          ctx.height=ctx.width*heightRatio;

// 3) create the chart using the chart canvas
        var myChart = new Chart(ctx, {
                                        type: chartType,
                                        data: chartData,
                                        options:{
                                            scales: {
                                                        y:{
                                                            stacked: stacked_status,
                                                            ticks:{
                                                                callback: function(value) {
                                                                    return value.toLocaleString('en-UK', {style:'currency', currency:'GBP', maximumFractionDigits:0});
                                                                                            }
                                                                    },
                                                             },
                                                        x:{
                                                            stacked: stacked_status,
                                                            ticks:{

                                                                    }
                                                             },
                                                     }
                                                 }
                                 });


    return(myChart);
}