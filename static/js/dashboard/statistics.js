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

var remaining_time = {
  election: 0,
  result: 0
}

var startCountdown = function(section) {
  var countdownInterval = setInterval(function() {
      if (remaining_time[section] > 0) {
          remaining_time[section] -= 1
          document.getElementById(`${section}-remaining-time`).innerHTML = new Date(remaining_time[section] * 1000).toISOString().substr(11, 8)
      }
      else {
          clearInterval(countdownInterval)
          document.getElementById(`${section}-remaining-time`).innerHTML = '00:00:00'
      }
  }, 1000)
}

function setStatus(response, section) {
  result = JSON.parse(response).result
  document.getElementById(`${section}-status`).innerHTML = result.status;
  document.getElementById(`${section}-start`).innerHTML = (new Date(result.start)).toLocaleString();
  document.getElementById(`${section}-end`).innerHTML = (new Date(result.end)).toLocaleString();

  if (Math.abs(remaining_time[section] - result['remaining_time']) > 3) {
    if (remaining_time[section] === 0) {
        remaining_time[section] = result['remaining_time']
        startCountdown(section)
    }
    else {
        remaining_time[section] = result['remaining_time']
    }
  }

  switch (result.status.toLowerCase()) {
    case 'Finished'.toLowerCase():
      document.getElementById(`${section}-status`).setAttribute('class', 'text-success')
      break;
    
    case 'In Progress'.toLowerCase():
      document.getElementById(`${section}-status`).setAttribute('class', 'text-warning')
      break;
    
    case 'Not Started Yet'.toLowerCase():
      document.getElementById(`${section}-status`).setAttribute('class', 'text-info')
      break;
      
    default:
      document.getElementById(`${section}-status`).setAttribute('class', '')
      break;
  }
}

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

}

loop()

var myInterval = setInterval(loop, 5000);
