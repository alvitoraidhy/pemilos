var stringToColour = function(str) {
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    var colour = '#';
    for (var i = 0; i < 3; i++) {
      var value = (hash >> (i * 8)) & 0xFF;
      colour += ('00' + value.toString(16)).substr(-2);
    }
    return colour;
}

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
      position: 'top',
      labels: {
        fontSize: 14,
        fontColor: '#111'
      }
    },
    cutoutPercentage: 0,
  }
}

var resultChart = new Chart(ctx, chartData);

function loop() {
    // Result Chart
    httpGetAsync(`${pemilos_url}/api/vote-result`, function(response) {
        result = JSON.parse(response).result
        var labels = [],
            data = [],
            backgroundColor = []

        for (var i = 0; i < result.candidates.length; i++){
            candidate = result.candidates[i]
            labels.push(candidate.name)
            data.push(candidate.votes)
            backgroundColor.push(stringToColour(candidate.name))
        }

        labels.push('Tidak Memilih')
        data.push(result.abstain_votes)
        backgroundColor.push('#dddddd')

        chartData.data.labels = labels
        chartData.data.datasets[0].data = data,
        chartData.data.datasets[0].backgroundColor = backgroundColor
        chartData.data.datasets[0].hoverBorderColor = "rgba(234, 236, 244, 1)"

        resultChart.update();

        var parent = document.getElementById(`candidate-data`)

        var candidateDatas = {}

        var candidateEls = parent.children
        for (var i = 0; i < candidateEls.length; i++) {
          candidateDatas[candidateEls[i].getAttribute('id')] = candidateEls[i]
        }
        
        for (var i = 0; i < result.candidates.length; i++) {
          var candidate = result.candidates[i]
          var el = document.getElementById(`candidate-${candidate.candidate_number}`)
          if (!el) {
            el = document.createElement('div')
            el.setAttribute('id', `candidate-${candidate.candidate_number}`)
            el.classList.add('col-md-6')
            el.classList.add('col-sm-12')
            el.classList.add('mx-auto')
            el.classList.add('p-3')

            el.innerHTML = `
              <div class="card">
                <div class="card-header font-weight-bold text-center">
                  <span id="candidate-${candidate.candidate_number}-name">${candidate.name}</span>
                </div>
                <div class="card-body text-center">
                  <p>
                    <strong><span id="candidate-${candidate.candidate_number}-vote">${candidate.votes}</span></strong> vote(s)
                  </p>
                </div>
              </div>
            `

            parent.appendChild(el)
          }

          else {
            candidateName = document.getElementById(`candidate-${candidate.candidate_number}-name`)
            candidateName.innerHTML = `${candidate.name}`

            candidateVote = document.getElementById(`candidate-${candidate.candidate_number}-vote`)
            candidateVote.innerHTML = `${candidate.votes}`

            delete candidateDatas[`candidate-${candidate.candidate_number}`]
          }
        }


        for (var i = 0; i < candidateDatas.keys; i++) {
          key = candidateDatas.keys[i]
          parent.removeChild(candidateDatas[key])
        }
    })
}

loop()

var myInterval = setInterval(loop, 5000);
