function genericScatterPlotData(data) {
    var data_list = data.value
    var categories = data.category
    var series = [];
    for (j = 0; j < categories.length; j++) {
        var data_i = {
            type: 'scatter',
            name: categories[j],
            data: data_list[j],
        };
        series.push(data_i);
    }
    return series
}

function genericlineData(data) {
    var data_list = data.value
    var categories = data.category
    var series = [];
    for (j = 0; j < categories.length; j++) {
        var data_i = {
            name: categories[j],
            data: data_list[j],
        };
        series.push(data_i);
    }
    return series
}
