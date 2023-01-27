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
            itemMarginBottom: 3,
            itemWidth: 180,
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
        series:data,
        exporting: exportContextMenu
      });
    
}

function genericBarChart(data, div_id, chart_title, chart_sub_title, xAxisTitle,yAxisTitle) {

    Highcharts.chart(div_id, {
        chart: {
            type: 'column',
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
                text: null
            }
        },
        yAxis: {
            title: {
                enabled: true,
                text: yAxisTitle
            }
        },
        tooltip: {
            valueSuffix: 'Meters'
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -20,
            y: 80,
            floating: true,
            borderWidth: 1,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
            shadow: true
        },
        credits: {
            enabled: false
        },
        colors: ['#234a83', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
        series:data.value,
        exporting: exportContextMenu
    });
    
}

