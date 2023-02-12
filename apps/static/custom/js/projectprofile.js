
$(document).ready(function () {
  for (i = 0; i < chartlist.length; i++) {
      chartnumber = i+2
      id = '#'+chartnumber.toString()+'chart'
      $(id).removeClass('hide');
      chartvalues = chartjson[chartlist[i]]
      userChartDrawFunctionStatic(chartlist[i],chartvalues.ags,chartvalues.v1,chartvalues.v2,chartvalues.classtype,chartvalues.chart,chartvalues.ags_text);
    } 
  function userChartDrawFunctionStatic(chartDiv,ags,v1,v2,classtype,chart,ags_text) {
    var dataRequest = {
      ags: ags,
      v1: v1,
      v2: v2,
      classtype: classtype,
      chart: chart
    };
    $.get("/project/ajax-chart", dataRequest).done(function (data) {
      var data = data.chart_data;
      yaxis = v1.split("Vs")[0];
      if(v1=='Particle Size'){
        var arranged_data = genericlineData(data)
        genericLineChart(arranged_data, chartDiv, v1 + " vs " + v2, "Derived from " + ags_text+ " for " +classtype, 'SIZE', 'PERP')
      }
      else if(v1== 'Water Level'){
        genericBarChart(data, chartDiv, v1 + " vs " + v2, "Derived from " + ags_text, 'Bore Hole', 'Elevation (MSL)')
      }
      else{
        var arranged_data = genericScatterPlotData(data)
        genericScatterPlot(arranged_data, chartDiv, v1 + " vs " + v2, "Derived from " + ags_text, yaxis, 'Elevation (MSL)',)
      }
    });
  };


})