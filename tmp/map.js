const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

var map = L.map('mapid').setView([0, 0], 0)

const tiles = L.tileLayer(tileUrl, { 
    reuseTiles: true,
    preferCanvas: true,
    // bounds: bounds,
    updateWhenZooming: false,
    detectRetina: true,
    minZoom: 4,
    maxZoom: 15,
    // maxBounds: bounds,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' 
}).addTo(map)

// $(function() {
//     $(".button").click(function(){
//         var dataString = 
//             "minimal_latitude=" + $("input#min_lat").val() +
//             "&maximal_latitude=" + $("input#max_lat").val() +
//             "&minimal_longitude=" + $("input#min_lon").val() +
//             "&maximal_longitude=" + $("input#max_lon").val() +
//             "&date_from=" + $("input#date_from").val() +
//             "&date_to=" + $("input#date_to").val()
//         $.ajax({
//             url: "/handle",
//             type: "get",
//             data: dataString,
//             dataType: "json",
//             success: function(response) {
//                 var data = response
                
//                 var points = []
//                 var minC = 380;
//                 console.log(data)
                                            
//                 for (var month in data['months']) {
//                     for (var index = 0; index < data['months'][month].length; index++) {
//                         if (data['months'][month][index][5] < minC) {
//                             points.push(
//                                 [data['months'][month][index][3], data['months'][month][index][4], 0]
//                             )
//                         } else {
//                             points.push(
//                                 [data['months'][month][index][3], data['months'][month][index][4], data['months'][month][index][5] - minC]
//                             )
//                         }
//                     }
//                 }

//                 console.log(points)

//                 var heat = L.idwLayer(points, {
//                     opacity: 0.3,
//                     maxZoom: 5,
//                     cellSize: 16,
//                     exp: 4,
//                     max: 410 - minC,
//                     gradient: {
//                         0.0: 'blue',
//                         0.25: 'cyan',
//                         0.5: 'lime',
//                         0.75: 'yellow',
//                         1: 'red'
//                     }
//                 }).addTo(map)
//             },
//             error: function(xhr) {
//                 alert('not stonks!');
//             }
//         });
//         return false;
//     });
// });