const pemilos_url = 'http://localhost:8000'

function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.withCredentials = true;
    xmlHttp.send(null);
}

function classPercentage(response, classname) {
  result = JSON.parse(response).result[classname]
  document.getElementById(`class-${classname}-text`).innerHTML = result;
  if (result !== '-') {
    document.getElementById(`class-${classname}-bar`).setAttribute('aria-valuenow', result.slice(0,-21));
    document.getElementById(`class-${classname}-bar`).style.width = result;
  }
  else {
    document.getElementById(`class-${classname}-bar`).setAttribute('aria-valuenow', '0');
    document.getElementById(`class-${classname}-bar`).style.width = '0%';
  }
}

function setStatus(response, section) {
  result = JSON.parse(response).result
  document.getElementById(`${section}-status`).innerHTML = result.status;
  document.getElementById(`${section}-start`).innerHTML = result.start;
  document.getElementById(`${section}-end`).innerHTML = result.end;

  switch (result.status.toLowerCase()) {
    case 'Finished'.toLowerCase():
      document.getElementById(`${section}-status`).setAttribute('class', 'text-success')
      break;
    
    case 'In Progress'.toLowerCase():
      document.getElementById(`${section}-status`).setAttribute('class', 'text-warning')
      break;
    
    case 'Not Started Yet'.toLowerCase():
      document.getElementById(`${section}-status`).setAttribute('class', 'text-info')
      document.getElementById(`${section}-status`).innerHTML = result.status
      break;
      
    default:
      document.getElementById(`${section}-status`).setAttribute('class', '')
      break;
  }
}

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Result Chart
var ctx = document.getElementById("resultChart");
var chartData = {
  type: 'pie',
  data: {
    labels: [],
    datasets: [{}],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: true,
      position: 'right',
      labels: {
        fontSize: 14
      }
    },
    cutoutPercentage: 0,
  }}
var resultChart = new Chart(ctx, chartData);

function loop() {
  // Total Students
  httpGetAsync(`${pemilos_url}/api/total-students`, function(response) {
    document.getElementById('total-students').innerHTML = JSON.parse(response).result;
  })

  // Has Voted
  httpGetAsync(`${pemilos_url}/api/has-voted`, function(response) {
    document.getElementById('has-voted').innerHTML = JSON.parse(response).result;
  })

  // Hasn't Voted
  httpGetAsync(`${pemilos_url}/api/hasnt-voted`, function(response) {
    document.getElementById('hasnt-voted').innerHTML = JSON.parse(response).result;
  })

  // Election Status
  httpGetAsync(`${pemilos_url}/api/election-info`, function(response) { setStatus(response, 'election' )})

  // Result Status
  httpGetAsync(`${pemilos_url}/api/result-info`, function(response) { setStatus(response, 'result' )})

  // Class Percentage
  httpGetAsync(`${pemilos_url}/api/grade-vote-percentage`, function(response) {
    classPercentage(response, 'x')
    classPercentage(response, 'xi')
    classPercentage(response, 'xii')
  })

  // Result Chart
  httpGetAsync(`${pemilos_url}/api/vote-result`, function(response) {
    result = JSON.parse(response).result
    console.log(result)
    var labels = [],
      data = [],
      backgroundColor = []

    for (var i = 0; i < result.candidates.length; i++){
      candidate = result.candidates[i]
      labels.push(candidate.name)
      data.push(candidate.votes)
      backgroundColor.push("#" + candidate.name.toString(16).padStart(6, '0'))
    }

    labels.push('Abstain')
    data.push(result.abstain_votes)
    backgroundColor.push('#dddddd')

    chartData.data.labels = labels
    chartData.data.datasets[0].data = data,
    chartData.data.datasets[0].backgroundColor = backgroundColor
    chartData.data.datasets[0].hoverBorderColor = "rgba(234, 236, 244, 1)"

    resultChart.update();
  })
}

loop()

var myInterval = setInterval(loop, 5000);
