// This Java-Script file contains the script which is responsible for 
// the functionalities and representations of the webmap.

//----------------------------------------
//--- Part 1: Adding a Basemap ----
//----------------------------------------

// Open Street map
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var osm = new L.tileLayer(osmUrl, {
	maxZoom: 17,
	attribution: osmAttrib
});

// Open Tope map
var OpenTopoMap = L.tileLayer('http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
	maxZoom: 17,
	attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
});

googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});

//----------------------------------------
//--- Part 2: Adding a GeoJSON ----
//----------------------------------------
// custom icon
var smallIcon = L.icon({
	iconSize: [27, 27],
	iconAnchor: [13, 27],
	popupAnchor:  [1, -24],
	iconUrl: 'img/loca.png'
});


function onEachFeature(feature, layer) {
	layer.on({
		mouseover: function () {
			this.setStyle({
				'fillColor': '#b45501',
			});
		}
	});
	layer.bindTooltip(feature.properties.name, {permanent:true,direction:'center',className: 'countryLabel'});        
	 }




//----------------------------------------
//--- Part 3: Adding a Basemap and overlay map ----
//----------------------------------------
// Overlay to visualize geojson


// Base Map group
var baseMaps = {
	"Satellite Basemap": googleSat,
	"Open Street Map": osm
};

// define Leaflet map object
var map = L.map('detail-map', {
	zoom: 17,
	layers: [googleSat],
	fullscreenControl: true,
	fullscreenControlOptions: {
		position: 'topleft'
	}
});

let overlayMaps = {}
let arrayOfMarkers = [];
let arrayOfColor = []
for (var i = 0; i < hole_list.length; i++) {

	for (let j = 0; j < hole_data[hole_list[i]].features.length; j++) {
		arrayOfMarkers.push([hole_data[hole_list[i]].features[j].geometry.coordinates[1], hole_data[hole_list[i]].features[j].geometry.coordinates[0]])
	  }
	var randomColor = "#" + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0').toUpperCase()
	arrayOfColor.push(randomColor)
	hole_layer = L.geoJson(hole_data[hole_list[i]], {
		style:{color:randomColor},
		pointToLayer: function (feature, latlng) {
			smallIcon
			return L.circleMarker(latlng,{radius:6});
		},
		onEachFeature: async function (feature, layer) {
			layer.bindPopup('Hole ID: <h6>'+feature.properties.id +'</h6>Latitude: <h6>'+feature.properties.lat +'</h6>Longitude: <h6>'+feature.properties.lon +'</h6><br /><button class="btn btn-primary" id="drawChart-first-apply"><i class="material-icons">draw</i> Draw-1</button><br /><br /><button class="btn btn-primary" id="drawChart-first-apply"><i class="material-icons">draw</i> Draw-2</button>');
			layer.bindTooltip(feature.properties.id);
		}
	}).addTo(map);

	overlayMaps[hole_list[i]] = hole_layer;
}

//----------------------------------------
//--- Part 4: Adding a Extra Functionality ----
//----------------------------------------

// Adding Layer control
var layerControl = L.control.layers(baseMaps, overlayMaps).addTo(map);
// console.log(arrayOfMarkers)
var bounds = new L.LatLngBounds(arrayOfMarkers);
map.fitBounds(bounds);
// Home buttom
L.easyButton('fa-home', function (btn, map) {
	map.fitBounds(bounds);
}, 'Zoom To Home').addTo(map);

// Scale Bar
L.control.scale().addTo(map)

L.control.locate().addTo(map);

var legend = L.control({position: 'bottomright'});
legend.onAdd = function (map) {

var div = L.DomUtil.create('div', 'info legend');
labels = ['<strong>Legend</strong>'],
categories = hole_list;

div.innerHTML ='';
for (var i = 0; i < categories.length; i++) {
    labels.push(
        '<i class="circle" style="background:' + arrayOfColor[i] + '"></i> ' +
    (categories[i] ? categories[i] : '+'));

}
div.innerHTML = labels.join('<br>');
return div;
};
legend.addTo(map);







