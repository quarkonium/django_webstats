var chart;
var data_test;
jQuery(document).ready(function() {

  //alert(data_test['categories'
  var chart_data = {
    chart: {
      renderTo: 'page_views',
      defaultSeriesType: 'column',
      marginRight: 130,
      marginBottom: 30
    },
    title: {
      text: 'Average page views per visit',
      x: -20 //center
    },
    subtitle: {
      text: '',
      x: -20
    },
    xAxis: {
    },
    yAxis: {
      title: {
        text: 'page views'
      },
      plotLines: [{
        value: 0,
        width: 1,
        color: '#808080'
      }]
    },
    tooltip: {
      formatter: function() {
        return ''+ this.series.name +''+this.x +': '+ this.y;
      }
    },
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'top',
      x: -10,
      y: 100,
      borderWidth: 0
    },
    series: [{
      name: 'Average page views'
        }]
  };

  chart_data['xAxis']['categories'] = data_test['categories'];
  
  chart_data['series'][0]['data'] = data_test['page_views_per_visit'];

  //alert(chart_data['xAxis']['categories']);
  //alert(JSON.stringify(chart_data));

  chart = new Highcharts.Chart(chart_data);
});
