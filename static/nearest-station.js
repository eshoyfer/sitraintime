var panel = document.getElementById("location-info");
var button = document.getElementById("button-container");

var options = {
  maximumAge: 0,
  enableHighAccuracy: true,
  timeout: Infinity,
};

function stationButtonHtml(station) {
    stationUrlString = station.toLowerCase().replace(' ', '_').replace("'", '');
    var buttonHtmlTemplate ='\
        <a href="/station/STATION_HERE" style="width: 100%"  type="button" class="btn btn-primary btn-lg"> \
          <span class="glyphicon glyphicon-map-marker"></span> Use current location \
        </a>';
    var buttonHtml = buttonHtmlTemplate.replace("STATION_HERE", stationUrlString);
    return buttonHtml;
};

// Euclidean distance between two points
// For small distances, Euclidean distance on an equirectangular projection works as an approximation
// (No need to go all out with the haversine or law of cosines formula)
function distance(lat1, long1, lat2, long2) {
    var R = 3959; // Earth's radius in miles
    var x = (long2 - long1) * Math.cos((lat1 + lat2)/2);
    var y = lat2 - lat1;
    var d = Math.sqrt(x*x + y*y) * R;
    return d;
};

var coords = {
    "Tottenville": [40.512772, -74.251964],
    "Atlantic": [40.516311, -74.245784],
    "Nassau": [40.518465, -74.238403],
    "Richmond Valley": [40.519606, -74.229090],
    "Pleasant Plains": [40.522608, -74.218018],
    "Prince's Bay": [40.525438, -74.200101],
    "Huguenot": [40.533587, -74.191840],
    "Annadale": [40.540570, -74.178261],
    "Eltingville": [40.544526, -74.164582],
    "Great Kills": [40.552092, -74.151364],
    "Bay Terrace": [40.556746, -74.136875],
    "Oakwood Heights": [40.566177, -74.126301],
    "New Dorp": [40.573514, -74.117214],
    "Grant City": [40.579756, -74.109790],
    "Jefferson Av": [40.584645, -74.103481],
    "Dongan Hills": [40.589677, -74.096034],
    "Old Town": [40.596586, -74.087322],
    "Grasmere": [40.603135, -74.084190],
    "Clifton": [40.621379, -74.071487],
    "Stapleton": [40.628936, -74.075092],
    "Tompkinsville": [40.637795, -74.074791],
    "St George": [40.643786, -74.073632]
};

function nearestStation(lat1, long1) {
    var shortestDistance = -1;
    var closestStation;
    for (station in coords) {
      var stationCoords = coords[station];
      var stationLat = stationCoords[0];
      var stationLong = stationCoords[1];
      var thisDistance = distance(lat1, long1, stationLat, stationLong);
      if ((shortestDistance === -1) || (thisDistance < shortestDistance)) {
        closestStation = station;
        shortestDistance = thisDistance;
      } 
    }
    return closestStation;
};
  

function getLocation() {
    if (navigator.geolocation) {
        positionRequest = navigator.geolocation.getCurrentPosition(success, failure, options);
    } else {
        panel.innerHTML = "Your browser does not support this feature. Select a station below.";
    }
};

function success(position) {
    var coordinates = position.coords;
    var closestStation = nearestStation(coordinates.latitude, coordinates.longitude);
    panel.innerHTML = "Your nearest station is: <strong>" + closestStation + "</strong>";
    button.innerHTML = stationButtonHtml(closestStation);
};

function failure(position_error) {
    panel.innerHTML = "Unable to determine your location. Select a station below.";

};

getLocation();