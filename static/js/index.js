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

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

function animate(size='0%', callback=function(){}) {
    document.getElementsByClassName('south west block layer-2')[0].style.width = size;
    setTimeout( function() {
        document.getElementsByClassName('south east block layer-2')[0].style.height = size;
        setTimeout( function() {
            document.getElementsByClassName('north east block layer-2')[0].style.width = size;
            setTimeout( function() {
                document.getElementsByClassName('north west block layer-2')[0].style.height = size;
                setTimeout(callback, 1000)
            }, 1000);
        }, 1000);
    }, 1000);
}

function setColor(className, color) {
    var els = document.getElementsByClassName(`${className}`)

    for (var i = 0; i < els.length; i++) {
        els[i].style['background-color'] = color
    }
}

function open(callback) {
    animate(size='0%', callback=callback)
}

function close(callback) {
    animate(size='50%', callback=callback)
}

function loop() {
    open(function() {
        setColor('layer-2', getRandomColor())
        close(function() {
            setColor('layer-1', getRandomColor())
            loop()
        })
    })
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
        document.getElementById(`${section}-status`).innerHTML = "Selesai";
        document.getElementById(`${section}-status`).setAttribute('class', 'text-success')
        document.getElementById(`${section}-link`).classList.add('disabled')
        break;
      
      case 'In Progress'.toLowerCase():
        document.getElementById(`${section}-status`).innerHTML = "Sedang Berlangsung";
        document.getElementById(`${section}-status`).setAttribute('class', 'text-warning')
        document.getElementById(`${section}-link`).classList.remove('disabled')
        break;
      
      case 'Not Started Yet'.toLowerCase():
        document.getElementById(`${section}-status`).innerHTML = "Belum Dibuka";
        document.getElementById(`${section}-status`).setAttribute('class', 'text-info')
        document.getElementById(`${section}-link`).classList.add('disabled')
        break;
        
      default:
        break;
    }
}

function interval() {
    // Election Status
    httpGetAsync(`${pemilos_url}/api/election-info`, function(response) { setStatus(response, 'election' )})

    // Result Status
    httpGetAsync(`${pemilos_url}/api/result-info`, function(response) { setStatus(response, 'result' )})
}

var myInterval = setInterval(interval, 5000)


loop()
interval()
