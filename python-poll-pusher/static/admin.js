var dataPoints = [
{ label: "Tom Brady", y: 0 },
{ label: "Drew Brees", y: 0 },
{ label: "Peyton Manning", y: 0 },
{ label: "Brett Favre", y: 0 },
]

var chartContainer = document.querySelector('#chartContainer');

if (chartContainer) {
var chart = new CanvasJS.Chart("chartContainer", {
    animationEnabled: true,
    theme: "theme2",
    data: [
    {
        type: "column",
        dataPoints: dataPoints
    }
    ]
});

chart.render();
}

Pusher.logToConsole = true;

// Configure Pusher instance
const pusher = new Pusher('12ea89a2e687c7d8aa06', {
cluster: 'us2',
encrypted: true
});

// Subscribe to poll trigger
var channel = pusher.subscribe('poll');

// Listen to vote event
channel.bind('vote', function(data) {
dataPoints = dataPoints.map(dataPoint => {
    if(dataPoint.label == data[4].name[0]) {
    dataPoint.y += 10;
    }

    return dataPoint
});

// Re-render chart
chart.render()
});