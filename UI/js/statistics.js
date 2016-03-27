setTheme();

//Later retrieve the actual vale
var predictedSentiData = [];

var predictedPosData = {
  name: 'Positive',
  y: 155
};

predictedSentiData.push(predictedPosData);

var predictedNeuData = {
  name: 'Neutral',
  y: 2217
};

predictedSentiData.push(predictedNeuData);

var predictedNegData = {
  name: 'Negative',
  y: 196
};

predictedSentiData.push(predictedNegData);



$('#sentiPie').highcharts({
  chart: {
    plotBackgroundColor: null,
    plotBorderWidth: null,
    plotShadow: false,
    type: 'pie'
  },
  title: {
    text: 'Predicted Sentiment Distribution'
  },
  tooltip: {
    pointFormat: '<b>{point.percentage:.1f}%</b>'
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
        style: {
          color: Highcharts.theme && Highcharts.theme.contrastTextColor || 'black'
        }
      }
    }
  },
  series: [{
    colorByPoint: true,
    data: predictedSentiData
  }]
});

var trueSentiData = [];
var truePosData = {
  name: 'Actual Positive',
  //4 are classified as positive, 1 is classified as neural, 2 are classified as negative.
  data: [70, 359, 38]
};

trueSentiData.push(truePosData);

var trueNeuData = {
  name: 'Actual Neutral',
  //1 are classified as positive, 4 is classified as neural, 2 are classified as negative.
  data: [50, 1461, 75]
};

trueSentiData.push(trueNeuData);

var trueNegData = {
  name: 'Actual Negative',
  //2 are classified as positive, 3 is classified as neural, 8 are classified as negative.
  data: [35, 397, 83]
};

trueSentiData.push(trueNegData);

$('#sentiBar').highcharts({
  chart: {
    type: 'bar'
  },
  title: {
    text: 'Classification Detail'
  },
  xAxis: {
    categories: ['Predicted Positive', 'Predicted Neutral', 'Predicted Negative']
  },
  yAxis: {
    min: 0,
    title: {
      text: 'Count'
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
  series: trueSentiData
});

function setTheme() {
  Highcharts.theme = {
    colors: ['#DDDF0D', '#55BF3B', '#DF5353', '#7798BF', '#aaeeee', '#ff0066', '#eeaaee',
      '#55BF3B', '#DF5353', '#7798BF', '#aaeeee'],
    chart: {
      backgroundColor: {
        linearGradient: {
          x1: 0,
          y1: 0,
          x2: 1,
          y2: 1
        },
        stops: [
          [0, 'rgb(48, 48, 96)'],
          [1, 'rgb(0, 0, 0)']
        ]
      },
      borderColor: '#000000',
      borderWidth: 2,
      className: 'dark-container',
      plotBackgroundColor: 'rgba(255, 255, 255, .1)',
      plotBorderColor: '#CCCCCC',
      plotBorderWidth: 1
    },
    title: {
      style: {
        color: '#C0C0C0',
        font: 'bold 26px "Trebuchet MS", Verdana, sans-serif'
      }
    },
    subtitle: {
      style: {
        color: '#666666',
        font: 'bold 20px "Trebuchet MS", Verdana, sans-serif'
      }
    },
    xAxis: {
      gridLineColor: '#333333',
      gridLineWidth: 1,
      labels: {
        style: {
          color: '#A0A0A0'
        }
      },
      lineColor: '#A0A0A0',
      tickColor: '#A0A0A0',
      title: {
        style: {
          color: '#CCC',
          fontWeight: 'bold',
          fontSize: '18px',
          fontFamily: 'Trebuchet MS, Verdana, sans-serif'

        }
      }
    },
    yAxis: {
      gridLineColor: '#333333',
      labels: {
        style: {
          color: '#A0A0A0'
        }
      },
      lineColor: '#A0A0A0',
      minorTickInterval: null,
      tickColor: '#A0A0A0',
      tickWidth: 1,
      title: {
        style: {
          color: '#CCC',
          fontWeight: 'bold',
          fontSize: '18px',
          fontFamily: 'Trebuchet MS, Verdana, sans-serif'
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.75)',
      style: {
        color: '#F0F0F0'
      }
    },
    toolbar: {
      itemStyle: {
        color: 'silver'
      }
    },
    plotOptions: {
      line: {
        dataLabels: {
          color: '#CCC'
        },
        marker: {
          lineColor: '#333'
        }
      },
      spline: {
        marker: {
          lineColor: '#333'
        }
      },
      scatter: {
        marker: {
          lineColor: '#333'
        }
      },
      candlestick: {
        lineColor: 'white'
      }
    },
    legend: {
      itemStyle: {
        font: '12pt Trebuchet MS, Verdana, sans-serif',
        color: '#A0A0A0'
      },
      itemHoverStyle: {
        color: '#FFF'
      },
      itemHiddenStyle: {
        color: '#444'
      }
    },
    credits: {
      style: {
        color: '#666'
      }
    },
    labels: {
      style: {
        color: '#CCC'
      }
    },

    navigation: {
      buttonOptions: {
        symbolStroke: '#DDDDDD',
        hoverSymbolStroke: '#FFFFFF',
        theme: {
          fill: {
            linearGradient:
            {
              x1: 0,
              y1: 0,
              x2: 0,
              y2: 1
            },
            stops: [
              [0.4, '#606060'],
              [0.6, '#333333']
            ]
          },
          stroke: '#000000'
        }
      }
    },

    // scroll charts
    rangeSelector: {
      buttonTheme: {
        fill: {
          linearGradient: {
            x1: 0,
            y1: 0,
            x2: 0,
            y2: 1
          },
          stops: [
            [0.4, '#888'],
            [0.6, '#555']
          ]
        },
        stroke: '#000000',
        style: {
          color: '#CCC',
          fontWeight: 'bold'
        },
        states: {
          hover: {
            fill: {
              linearGradient:
              {
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1
              },
              stops: [
                [0.4, '#BBB'],
                [0.6, '#888']
              ]
            },
            stroke: '#000000',
            style: {
              color: 'white'
            }
          },
          select: {
            fill: {
              linearGradient: {
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1
              },
              stops: [
                [0.1, '#000'],
                [0.3, '#333']
              ]
            },
            stroke: '#000000',
            style: {
              color: 'yellow'
            }
          }
        }
      },
      inputStyle: {
        backgroundColor: '#333',
        color: 'silver'
      },
      labelStyle: {
        color: 'silver'
      }
    },

    navigator: {
      handles: {
        backgroundColor: '#666',
        borderColor: '#AAA'
      },
      outlineColor: '#CCC',
      maskFill: 'rgba(16, 16, 16, 0.5)',
      series: {
        color: '#7798BF',
        lineColor: '#A6C7ED'
      }
    },

    scrollbar: {
      barBackgroundColor: {
        linearGradient: {
          x1: 0,
          y1: 0,
          x2: 0,
          y2: 1
        },
        stops: [
          [0.4, '#888'],
          [0.6, '#555']
        ]
      },
      barBorderColor: '#CCC',
      buttonArrowColor: '#CCC',
      buttonBackgroundColor: {
        linearGradient: {
          x1: 0,
          y1: 0,
          x2: 0,
          y2: 1
        },
        stops: [
          [0.4, '#888'],
          [0.6, '#555']
        ]
      },
      buttonBorderColor: '#CCC',
      rifleColor: '#FFF',
      trackBackgroundColor: {
        linearGradient: {
          x1: 0,
          y1: 0,
          x2: 0,
          y2: 1
        },
        stops: [
          [0, '#000'],
          [1, '#333']
        ]
      },
      trackBorderColor: '#666'
    },

    // special colors for some of the
    legendBackgroundColor: 'rgba(0, 0, 0, 0.5)',
    background2: 'rgb(35, 35, 70)',
    dataLabelsColor: '#444',
    textColor: '#C0C0C0',
    maskColor: 'rgba(255,255,255,0.3)'
  };

  // Apply the theme
  var highchartsOptions = Highcharts.setOptions(Highcharts.theme);
}