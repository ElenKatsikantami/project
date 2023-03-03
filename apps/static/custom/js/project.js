
$(document).ready(function () {
    var headings_factual = headings.factual
    var headings_interpretation = headings.interpretation
  
    $('#select-variable-first').empty();
    for (i = 0; i < headings_factual.length; i++) {
      $('#select-variable-first').append($('<option>', { value: headings_factual[i], text: headings_factual[i] }));
    }
    
    $('#select-category').on('change', function (){
      $('#select-variable-first').empty();
      if($('#select-category').val() == 'factual'){
      for (i = 0; i < headings_factual.length; i++) {
        $('#select-variable-first').append($('<option>', { value: headings_factual[i], text: headings_factual[i] }));
      }}
      else{
      for (i = 0; i < headings_interpretation.length; i++) {
        $('#select-variable-first').append($('<option>', { value: headings_interpretation[i], text: headings_interpretation[i] }));
      }}})
  
    $('#select-variable-first').on('change', function () {
      $('#select-variable-second').empty()
      $('#select-class-type').empty()
      $('#select-chart').empty()
      if ($('#select-variable-first').val() == 'Particle Size') {
        $('#select-variable-second').append($('<option>', { value: 'Percentage Passing (%)', text: 'Percentage Passing (%)' }));
        get_borhole_list()
        $('#select-chart').append($('<option>', { value: 'Line Chart', text: 'Line chart' }));
      }
      else if ($('#select-variable-first').val() == 'Water Level') {
        $('#select-variable-second').append($('<option>', { value: 'Elevation', text: 'Elevation' }));
          general_key = ['By Bore Hole','By Machine Type','By Bore Hole and Machine Type']
          general_value = ['borehole','machine','boreholeandmachine']
          for (i = 0; i < general_value.length; i++) {
            $('#select-class-type').append($('<option>', { value: general_value[i], text: general_key[i] }));
          }
          $('#select-chart').append($('<option>', { value: 'barchart', text: 'Barchart' }));
      }
      else{
        $('#select-variable-second').append($('<option>', { value: 'Elevation', text: 'Elevation' }));
          $('#select-variable-second').append($('<option>', { value: 'Depth', text: 'Depth' }));
          general_key = ['By Bore Hole','By Machine Type','By Bore Hole and Machine Type']
          general_value = ['borehole','machine','boreholeandmachine']
          for (i = 0; i < general_value.length; i++) {
            $('#select-class-type').append($('<option>', { value: general_value[i], text: general_key[i] }));
          } 
          $('#select-chart').append($('<option>', { value: 'scatter plot', text: 'Scatter plot' }));
      }
    });
  
    $('#select-ags-file').on('change', function () {
      $('#select-variable-first').empty()
      $('#select-variable-second').empty()
      $('#select-class-type').empty()
      if($('#select-category').val() == 'factual'){
        for (i = 0; i < headings_factual.length; i++) {
          $('#select-variable-first').append($('<option>', { value: headings_factual[i], text: headings_factual[i] }));
        }}
      else{
        for (i = 0; i < headings_interpretation.length; i++) {
          $('#select-variable-first').append($('<option>', { value: headings_interpretation[i], text: headings_interpretation[i] }));
        }};
      $('#select-variable-second').append($('<option>', { value: 'Elevation', text: 'Elevation' }));
      $('#select-variable-second').append($('<option>', { value: 'Depth', text: 'Depth' }));
      general_key = ['By Bore Hole','By Machine Type','By Bore Hole and Machine Type']
      general_value = ['borehole','machine','boreholeandmachine']
      for (i = 0; i < general_value.length; i++) {
            $('#select-class-type').append($('<option>', { value: general_value[i], text: general_key[i] }));
          } 
        });
    
    var chartCounter = 6
    $('#extra-chart').click(function () {
      id = '#'+chartCounter.toString()+'chart'
      if(chartCounter == 12){
        $('#extra-chart').addClass('hide');
      }
      $(id).removeClass('hide');
      chartCounter = chartCounter+2
    });
  
    $('#drawChart-first-apply').click(function () {
      userChartDrawFunction("drawChart-first");
    });
    $('#drawChart-second-apply').click(function () {
      userChartDrawFunction("drawChart-second");
    });
    $('#drawChart-third-apply').click(function () {
      userChartDrawFunction("drawChart-third");
    });
    $('#drawChart-fourth-apply').click(function () {
      userChartDrawFunction("drawChart-fourth");
    });
  
    $('#drawChart-five-apply').click(function () {
      userChartDrawFunction("drawChart-five");
    });
    $('#drawChart-six-apply').click(function () {
      userChartDrawFunction("drawChart-six");
    });
    $('#drawChart-seven-apply').click(function () {
      userChartDrawFunction("drawChart-seven");
    });
    $('#drawChart-eight-apply').click(function () {
      userChartDrawFunction("drawChart-eight");
    });
  
    $('#drawChart-nine-apply').click(function () {
      userChartDrawFunction("drawChart-nine");
    });
    $('#drawChart-ten-apply').click(function () {
      userChartDrawFunction("drawChart-ten");
    });
    $('#drawChart-eleven-apply').click(function () {
      userChartDrawFunction("drawChart-eleven");
    });
    $('#drawChart-twelve-apply').click(function () {
      userChartDrawFunction("drawChart-twelve");
    });  
    function userChartDrawFunction(chartDiv) {
      var chartinnerdict = {};
      var ags = $('#select-ags-file').val();
      var ags_text = $("#select-ags-file option:selected").text();
      var v1 = $('#select-variable-first').val();
      var v2 = $('#select-variable-second').val();
      var classtype = $('#select-class-type').val();
      var chart = $('#select-chart').val();
      chartinnerdict['ags'] = ags
      chartinnerdict['v1'] = v1
      chartinnerdict['v2'] = v2
      chartinnerdict['classtype'] = classtype
      chartinnerdict['chart'] = chart
      chartinnerdict['ags_text'] = ags_text
      chartdict[chartDiv] = chartinnerdict
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
  
    function get_borhole_list(){
      var ags = $('#select-ags-file').val();
      var dataRequest = {
        ags: ags
      };
      $.get("/project/borehole", dataRequest).done(function (data) {
        for (i = 0; i < data.boreholes.length; i++) {
            $('#select-class-type').append($('<option>', { value: data.boreholes[i], text: data.boreholes[i] }));
          }
      });
    };
  
    btn.onclick = function() {
      modal.style.display = "block";
      console.log(chartdict)
      $("#profilechartlist").val(JSON.stringify(chartdict, null, 2));
      $("#profileprojectname").val(projectname);
      $("#profileprojectid").val(projectid);
    }

    span.onclick = function() {
      modal.style.display = "none";
    }

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
  
})