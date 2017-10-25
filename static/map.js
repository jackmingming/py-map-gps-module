/*
  [37.78549, -122.46097]
 */

var map;
var userMarker;
var markerPosition;
var enemiesMarker = {};
var popup;
var layer;


var source = new EventSource('/api/sse/state');

function initMap() {
    map = L.map('map');
    layer = L.tileLayer('http://192.168.65.154/osm_tiles/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);
    L.control.scale().addTo(map);
    userMarker = createMarker('/static/images/navigation_128.png', [32, 32]);
    setMapView([37.78549, -122.46097], 16)
    setUserMarkerPosition([37.78549, -122.46097], 90);
    if (typeof MainWindow != 'undefined') {
        map.on('move', onMapMove);
        onMapMove();
    }
}

function onMapMove() {
    MainWindow.onMapMove(map.getCenter().lat, map.getCenter().lng)
}

function setMapView(data, zoom) {
    map.setView(data, zoom);
}

function createMarker(url, size) {
    var icon = L.icon({
        iconUrl: url,
        iconSize: size,
    });

    return icon;
}

function setUserMarkerPosition(position, rotation) {
    L.marker(position, {
        icon: userMarker,
        rotationAngle: rotation,
        rotationOrigin: 'center center',
    }).addTo(map);
}

initMap()

source.onmessage = function(event) {
    var position = JSON.parse(event.data);

};