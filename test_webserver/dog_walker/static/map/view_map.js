var mymap = L.map('mapid', {
center:[50.44722980684235, -104.61782455444336],
zoom: 12,
minZoom: 12,
maxZoom: 18,
});

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const tiles = L.tileLayer(tileUrl, { attribution });
tiles.addTo(mymap);

mymap.setMaxBounds(L.latLngBounds(L.latLng(50.396700704675396,-104.48101043701172), L.latLng(50.512771567674484, -104.732666015625)));
mymap.setMaxZoom = 13;

//L.icon({
//        iconUrl: '/static/map/bone_pin.png',
//        iconSize:     [20, 20], // size of the icon
//        iconAnchor:   [0, 20], // point of the icon which will correspond to marker's location
//        popupAnchor:  [0, 20] // point from which the popup should open relative to the iconAnchor
//        });
//L.marker([poi[0].lat, poi[0].lng], {icon: bonePin}).addTo(mymap);
//poi = document.get
//console.log(poi);


mymap.on('click', function(e){
  var latlng = mymap.mouseEventToLatLng(e.originalEvent);
  console.log(latlng.lat + ', ' + latlng.lng);

  const bonePin = L.icon({
        iconUrl: '/static/map/bone_pin.png',
        iconSize:     [20, 20], // size of the icon
        iconAnchor:   [0, 20], // point of the icon which will correspond to marker's location
        popupAnchor:  [0, 20] // point from which the popup should open relative to the iconAnchor
    });
    L.marker([latlng.lat, latlng.lng], {icon: bonePin}).addTo(mymap);
});

L.geoJSON().addTo(mymap);

