// for (var i = 0; i < tempList.length; i++) {
//     L.marker([tempList[i][0], tempList[i][1]]).addTo(map)
// }
// L.marker(tempList).addTo(map)

// for (var i = 0; i < 30; i++) {
//     console.log(data['points'][i])
//     var idw = L.idwLayer([
//         [data['points'][i][3], data['points'][i][4], data['points'][i][5] / 1000.0]
//     ], {
//         radius: 25, 
//         max: 1.0,
//         gradient: {
//             0.4: 'blue',
//             0.65: 'lime',
//             1: 'red'
//         }
//     }).addTo(map);
// }

// layers = []

// for (var i = 0; i < trianglesList.length; i++) {
//     layers.push([])
//     for (var k = 0; k < trianglesList[i].length; k++) {
//         var idw = L.heatLayer([
//             [trianglesList[i][k][0][0], trianglesList[i][k][0][1], trianglesList[i][k][0][2] / 5.0],
//             [trianglesList[i][k][1][0], trianglesList[i][k][1][1], trianglesList[i][k][1][2] / 5.0],
//             [trianglesList[i][k][2][0], trianglesList[i][k][2][1], trianglesList[i][k][2][2] / 5.0]
//         ], {
//             opacity: 0.1, 
//             radius: 25, 
//             max: 50.0,
//             gradient: {
//                 0.4: 'blue',
//                 0.65: 'lime',
//                 1: 'red'
//             }
//         });
//         console.log(trianglesList[i][k])
//         layers[i].push(idw)
//         idw.addTo(map)
//     }
// }

// for (var i = 0; i < trianglesList.length; i++) {
//     layers.push([])
//     for (var k = 0; k < trianglesList[i].length; k++) {
//         var idw = L.idwLayer([
//             [trianglesList[i][k][0][0], trianglesList[i][k][0][1], 20],
//             [trianglesList[i][k][1][0], trianglesList[i][k][1][1], 25],
//             [trianglesList[i][k][2][0], trianglesList[i][k][2][1], 30]
//         ], {opacity: 0.1, cellSize: 10, exp: 4, max: 1200});
//         console.log(trianglesList[i][k])
//         layers[i].push(idw)
//         idw.addTo(map)
//     }
// }

// if (polygonsList.length > 0) {
//     var len = polygonsList.length;
//     for (var i = 0; i < len; i++) {
//         mymap.removeLayer(polygonsList.pop());
//     }
// }

// for (var i = 0; i < data[1].length; i++) {
//     var list = [
//         [data[1][i][0]['lat'], [data[1][i][0]['lon']]],
//         [data[1][i][1]['lat'], [data[1][i][1]['lon']]],
//         [data[1][i][2]['lat'], [data[1][i][2]['lon']]]
//     ]
//     var polygon = L.polygon(list, {color: 'red'});
//     polygonsList.push(polygon);
//     polygon.addTo(mymap);
// }
// console.log('polygons: ' + polygonsList.length);

// if (markers.length > 0) {
//     var len = markers.length;
//     for (var i = 0; i < len; i++) {
//         mymap.removeLayer(markers.pop())
//     }
// }

// for (var i = 0; i < data[0].length; i++) {
//     var marker = L.marker([data[0][i]['lat'], data[0][i]['lon']]);
//     markers.push(marker);
//     marker.addTo(mymap);
// }
// console.log('markers: ' + markers.length);