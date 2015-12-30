var chart;

var options = {
        chart: {
            renderTo: 'chart',
            type: 'column'
        },
        title: {
            text: 'Orders by day'
        },
        xAxis: {
            categories: []
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total orders received'
            }
        },
        legend: {
            reversed: true
        },
        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },
        series: []
    };

$(document).ready(function() {
    chart = new Highcharts.Chart(options);

    $.get("/admin/chartData", function(data) {
        console.log(data);
        options.xAxis.categories = data.xAxis
        options.series = data.series
        chart = new Highcharts.Chart(options);
    });

    $("#downloadButton").click(function(event) {
        window.location = "/admin/download"
    });
});
