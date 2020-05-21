let position = { minLat: 0, maxLat: 0, minLon: 0, maxLon: 0 };
let date = { timeFrom: "", timeTo: "" };
let zoom = 1, first = 0, second = 0;
let mymap = undefined;

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const tiles = L.tileLayer(tileUrl, { attribution });

if(mymap != undefined)
    mymap.remove();
mymap = L.map('mapID').setView([first, second], zoom);
position.minLat = first;
position.minLon = second;
tiles.addTo(mymap);