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
            // itemWidth: 180,
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

var pieColors = ['#234a83', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'];
function getPattern(i) {
    return {
        pattern: Highcharts.merge(Highcharts.patterns[i], {
            color: pieColors[i]
        })
    };
}

var patterns = [0, 1, 2, 3, 4].map(getPattern);

function genericStacChart(data, div_id, chart_title, chart_sub_title, xAxisTitle, yAxisTitle) {
    $('#'+div_id+'-1').addClass('hide')
    $('#'+div_id+'-2').removeClass('hide')
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
            min: 0,
            title: {
                text: yAxisTitle
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: ( // theme
                        Highcharts.defaultOptions.title.style &&
                        Highcharts.defaultOptions.title.style.color
                    ) || 'gray',
                    textOutline: 'none'
                }
            }
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: "horizontal",
            maxHeight: 40,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
            shadow: true
        },
        credits: {
            enabled: false
        },
        colors: patterns,
        series: [{
            name: 'BPL',
            data: [3]
        }, {
            name: 'FA Cup',
            data: [14]
        }, {
            name: 'CL',
            data: [10]
        }, {
            name: 'CL',
            data: [10]
        }, {
            name: 'CL',
            data: [10]
        }, {
            name: 'CL',
            data: [10]
        }, {
            name: 'CL',
            data: [10]
        }, {
            name: 'CL',
            data: [10]
        }, {
            name: 'CL',
            data: [10]
        }, {
            name: 'CL',
            data: [10]
        }],
        exporting: exportContextMenu
    });
    
}

function genericStacChartMultiple(data, div_id, chart_title, chart_sub_title, xAxisTitle, yAxisTitle) {
    $('#'+div_id+'-1').addClass('hide')
    $('#'+div_id+'-2').removeClass('hide')
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
            min: 0,
            title: {
                text: yAxisTitle
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: ( // theme
                        Highcharts.defaultOptions.title.style &&
                        Highcharts.defaultOptions.title.style.color
                    ) || 'gray',
                    textOutline: 'none'
                }
            }
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: "horizontal",
            maxHeight: 40,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
            shadow: true
        },
        credits: {
            enabled: false
        },
        colors: patterns,
        series: [{
            name: 'Norway',
            data: [148,102],
            stack: 'Europe'
        }, {
            name: 'Germany',
            data: [102,102],
            stack: 'Europe'
        }, {
            name: 'Spain',
            data: [102,102],
            stack: 'Europe'
        }, {
            name: 'Italy',
            data: [112,102],
            stack: 'Europe'
        }, {
            name: 'Greece',
            data: [102,102],
            stack: 'Europe'
        }],
        exporting: exportContextMenu
    });
    
}


