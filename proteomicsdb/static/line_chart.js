// specifies what each 'window.chartColors.color' means
window.chartColors = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(231,233,237)',
  yellow: 'rgb(255, 205, 86)',
};




function getNewChart(canvas, config) {
    return new Chart(canvas, config);
    }

var colorNames = Object.keys(window.chartColors);



function add_data(legend, data, i) {
      var colorName = colorNames[config.data.datasets.length % colorNames.length];
      var newColor = window.chartColors[colorName];

      var newDataset = {
        label: '',
        backgroundColor: newColor,
        borderColor: newColor,
        data: [],
        fill: false
      };

      newDataset.label = legend[i];
      newDataset.data = data[legend[i]] ;

      config.data.datasets.push(newDataset);
      window.myLine.update();

      i++
    };


