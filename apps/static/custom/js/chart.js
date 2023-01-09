//HIGHCHARTS EXPORT MENU
var exportContextMenu = {
    buttons: {
        contextButton: {
            menuItems: [{
                textKey: 'downloadPNG',
                onclick: function() {
                    this.exportChart();
                }
            }, {
                textKey: 'downloadJPEG',
                onclick: function() {
                    this.exportChart({
                        type: 'image/jpeg'
                    });
                }
            }, {
                textKey: 'downloadPDF',
                onclick: function() {
                    this.exportChart({
                        type: 'image/pdf'
                    });
                }
            }, {
                textKey: 'downloadCSV',
                onclick: function() {
                    this.downloadCSV();
                }
            }]
        }
    }
}

function genericScatterPlot(data, div_id, chart_title, chart_sub_title, xAxisTitle,yAxisTitle) {
    Highcharts.chart(div_id, {
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
          text: chart_title
        },
        subtitle: {
            text: chart_sub_title
        },
        xAxis: {
            categories: data.categories,
            title: {
                text: xAxisTitle,
                enabled: true
            }
        },
        yAxis: {
            title: {
                enabled: true,
                text: yAxisTitle
            }
        },
        credits: {
            enabled: false
        },
        legend: {
            layout: 'vertical',
            y: 20,
            align: 'right',
            verticalAlign: 'top',
            itemMarginTop: 3,
            itemMarginBottom: 3
        },
        colors: ['#234a83', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
        series: data,
        exporting: exportContextMenu
      });
    
}

function genericLineChart(data, div_id, chart_title, chart_sub_title, xAxisTitle,yAxisTitle) {
    Highcharts.chart(div_id, {
        chart: {
            type: 'spline',
            zoomType: 'xy'
        },
        title: {
          text: chart_title
        },
        subtitle: {
            text: chart_sub_title
        },
        xAxis: {
            categories: data.categories,
            title: {
                text: xAxisTitle,
                enabled: true
            }
        },
        yAxis: {
            title: {
                enabled: true,
                text: yAxisTitle
            }
        },
        credits: {
            enabled: false
        },
        legend: {
            layout: 'vertical',
            y: 20,
            align: 'right',
            verticalAlign: 'top',
            itemMarginTop: 3,
            itemMarginBottom: 3
        },
        colors: ['#234a83', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
        series: [{
            name: 'Tokyo',
            data: [[1.5,7], [2.3,9], [4.2,5.6]]
        }, {
            name: 'New York',
            data: [[0.8,9], [2.1,6.3], [5.0, 10.1]]
        }],
        exporting: exportContextMenu
      });
    
}

