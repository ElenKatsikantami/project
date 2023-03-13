
$(document).ready(function () {
  
  // genericStacChart("data", 'drawSectionChart-first', "test", "Derived from ", 'Section')
  // genericStacChart("data", 'drawSectionChart-second', "test", "Derived from ", 'Section')
  
})


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


var baseMaps = {
	"Satellite Basemap": googleSat,
	"Open Street Map": osm
};

// define Leaflet map object
var map = L.map('section-map', {
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
			layer.bindPopup('<div id="drawSectionChart-'+feature.properties.id+'-1" >Hole ID: <h6>'+feature.properties.id +
                      '</h6>Latitude: <h6>'+feature.properties.lat +
                      '</h6>Longitude: <h6>'+feature.properties.lon +
                      '</h6><br /><button class="btn btn-primary" id="drawSection" onclick='+
                      'genericStacChart("data","drawSectionChart-'+feature.properties.id+'","test","Derived","Section")'+'><i class="material-icons">draw</i>Draw Section</button>'+
                      '</div><div class="hide" id="drawSectionChart-'+feature.properties.id+'-2" ><div id="drawSectionChart-'+feature.properties.id+'" style="width:100%; height: 60vh;"></div></div>',
                      {closeOnClick: false, autoClose: false}).openPopup();
			layer.bindTooltip(feature.properties.id);
		}
	}).addTo(map);

	overlayMaps[hole_list[i]] = hole_layer;
}


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







