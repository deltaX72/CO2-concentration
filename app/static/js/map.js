//=====================================================================

var south, north, west, east, date_from, date_to, current_date

south = $("input#min_lat").val()
north = $("input#max_lat").val()
west = $("input#min_lon").val()
east = $("input#max_lon").val()
date_to = $("input#date_to").val()
current_date = $("input#date_from").val()

var layer = null
var borders = null
var pointsLayer = null
var pointsArray = []

var pointsJSON = null

//=====================================================================

const 
    southWest = L.latLng(-90, -180), 
    northEast = L.latLng(90, 200),
    bounds = L.latLngBounds(southWest, northEast),

    MIN_CON_VALUE = 380,
    MAX_CON_VALUE = 420

//=====================================================================

var map = L.map('mapid', {zoomControl: true}).setView(bounds.getCenter(), 5)
map.on('drag', () => {
    map.panInsideBounds(bounds, {animate: false})
})

const tiles = L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 
        reuseTiles: true,
        preferCanvas: true,
        updateWhenZooming: false,
        detectRetina: true,
        minZoom: 3,
        maxZoom: 15,
        bounds: bounds,
        maxBounds: bounds,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' 
}).addTo(map)

//=====================================================================

$("#send_id").click(function() {
    south = $("input#min_lat").val()
    north = $("input#max_lat").val()
    west = $("input#min_lon").val()
    east = $("input#max_lon").val()
    date_from = $("input#date_from").val()
    date_to = $("input#date_to").val()
    // point = $("input#point").val()
    quality = $("select#quality").val()

    current_date = $("input#date_from").val()

    $.ajax({
        url: "/handle",
        type: "get",
        data: 
            "&minimal_latitude=" + south + "&maximal_latitude=" + north +
            "&minimal_longitude=" + west + "&maximal_longitude=" + east +
            "&date_from=" + date_from + "&date_to=" + date_to + 
            // "&point=" + point + 
            "&quality=" + quality
        ,
        dataType: "json",
        success: function(data) {
            pointsJSON = data
            console.log(data)
            map.setView(L.latLngBounds(L.latLng(south, west), L.latLng(north, east)).getCenter(), 5)
            loadAndRenderMap(map, current_date)
        },
        error: function(xhr) {
            alert('Error!')
        }
    })
    return false
})

$("#next").click(function() {
    if (current_date == getDate(date_to, "current")) current_date = date_from
    else current_date = getDate(current_date, "next")
    // console.log(current_date + " vs " + date_from)
    // var date = current_date.split("-")
    // var _date = date_to.split("-")
    // console.log("date_to = " + date_to)
    // console.log("current_date = " + current_date)
    // if (date[0] == _date[0] && date[1] == _date[1]) date = date_from.split("-")
    // else {
    //     date = current_date.split("-")
    //     date[1] = parseInt(date[1]) + 1
    //     if (parseInt(date[1]) > 12) {
    //         date[0] = parseInt(date[0]) + 1
    //         date[1] = 1
    //     }
    // }
    // current_date = date[0].toString() + "-" + ((date[1] < 10) ? ("0" + parseInt(date[1])) : date[1]) + "-01"
    // console.log(current_date)
    loadAndRenderMap(map, current_date)
})

$("#prev").click(function() {
    // var date
    if (current_date == date_from) current_date = getDate(date_to, "current")
    else current_date = getDate(current_date, "prev")
    // console.log(current_date + " vs " + date_to)
    // if (current_date == date_from) date = date_to.split("-")
    // else {
    //     date = current_date.split("-")
    //     date[1] = parseInt(date[1]) - 1
    //     if (parseInt(date[1]) < 1) {
    //         date[0] = parseInt(date[0]) - 1
    //         date[1] = 12
    //     }
    // }
    // current_date = date[0].toString() + "-" + ((date[1] < 10) ? ("0" + parseInt(date[1])) : date[1]) + "-01"
    loadAndRenderMap(map, current_date)
})

function loadAndRenderMap(map, date) {
    if (layer != null)      map.removeLayer(layer)
    if (borders != null)    map.removeLayer(borders)
    // if (pointsLayer != null) map.removeLayer(pointsLayer)
    // if (pointsArray.length != 0) {
    //     const length = pointsArray.length
    //     for (var i = 0; i < length; i++) {
    //         map.removeLayer(pointsArray[i])
    //     }
    // }

    _date = date.split("-")
    _date[1] = parseInt(_date[1]).toString()
    // console.log(_date)

    var cSize = 25
    switch (quality) {
        case "Минимум": cSize = 16; break
        case "Среднее": cSize = 8; break
        case "Максимум": cSize = 4; break
    }
    layer = L.idwLayer(pointsJSON['periods'][_date[0]][_date[1]]['data'], {
        opacity: 0.3,
        cellSize: cSize,
        exp: 2,
        // max: pointsJSON['periods'][_date[0]][_date[1]]['max'] - pointsJSON['periods'][_date[0]][_date[1]]['min'],
        max: MAX_CON_VALUE - MIN_CON_VALUE,
        gradient: { 0.0: 'blue', 0.25: 'cyan', 0.5: 'lime', 0.75: 'yellow', 1: 'red' }
    })

    layer.addTo(map)

    // points = []
    // for (i in pointsJSON['periods'][_date[0]][_date[1]]['data']) {
    //     // console.log(i)
    //     const marker = new L.Marker([
    //         pointsJSON['periods'][_date[0]][_date[1]]['data'][i][0],
    //         pointsJSON['periods'][_date[0]][_date[1]]['data'][i][1],
    //         pointsJSON['periods'][_date[0]][_date[1]]['data'][i][2]
    //     ])
    //     marker.on('click', onMarkerClick)
    //     map.addLayer(marker)
    //     pointsArray.push(marker)
    // }

    const lines = [
        [[south, west], [north, west]],
        [[north, west], [north, east]],
        [[north, east], [south, east]],
        [[south, east], [south, west]]
    ]
    borders = L.polygon(
        lines,
        {color: 'black', opacity: 0.1}
    )
    borders.addTo(map)

    document.getElementById('current_date').value = current_date
    console.log(current_date.toString() + ", " + pointsJSON['periods'][_date[0]][_date[1]]['data'].length)
}

function checkIfDateUndefined(date) {

}

function getDate(_date, direction) {
    var date = _date.split("-")
    switch (direction) {
        case "prev": {
            date[1] = parseInt(date[1]) - 1
            if (parseInt(date[1]) < 1) {
                date[0] = parseInt(date[0]) - 1
                date[1] = 12
            }
            break;
        }
        case "next": {
            date[1] = parseInt(date[1]) + 1
            if (parseInt(date[1]) > 12) {
                date[0] = parseInt(date[0]) + 1
                date[1] = 1
            }
            break;
        }
        case "current": {
            date[2] = "01"
            break;
        }
        default: {
            console.log("Error! Current day has been returned!")
        }
    }
    return date[0].toString() + "-" + ((date[1] < 10) ? ("0" + parseInt(date[1])) : date[1]) + "-" + date[2]
}

function onMapClick(e) {
    // for ()
}

// function onMarkerClick(e) {
//     console.log(this.getLatLng())
// }

// function getLastDay(year, month) {
//     switch (month) {
//         case 1: return 31
//         case 2: return (year % 4 == 0) ? 29 : 28
//         case 3: return 31
//         case 4: return 30
//         case 5: return 31
//         case 6: return 30
//         case 7: return 31
//         case 8: return 31
//         case 9: return 30
//         case 10: return 31
//         case 11: return 30
//         case 12: return 31
//         default: return 0
//     }
// }



/*
    L.geoJSON({
        "type": "Feature",
        "properties": {
            "name": "It is me",
            "popUpContent": "Hehehe"
        },
        "geometry": {
            "type": "Point",
            "coordinates": pointsArray[i]
        }
    }).addTo(map)
*/  

/*
    ввод координат (min и max широта и долгота)
    ввод периода поиска данных (год, месяц, день; от даты - до даты)
    ввод единичного шага (день (маловато), неделя (может быть, но тоже маловато), месяц и так далее)
    переключение между шагами (кнопки вперед и назад для перехода на следующий и предыдущий шаг)

    добавить интервальную шкалу с цветовой палитрой значений концентрации 
        (на будущее, пока не требует реализации, потому шо я и армянин должны узнать, какие цвета должны использоваться в отрисовке)

    графики для исследований 
        (добавить график (кнопка); пока пусть будет только кнопка, какие графики будут - решим позже)
    вкл/выкл отображение точек на карте для исследования динамики изменений концентрации
        (переключатель отображения точек на карте; кнопка / ползунок / checkbox (квадратик с галочкой))

    настройки отрисовки на карте:
        выбор качества отрисовки (мин, ср, макс)
    
    ВСЕ ЭТО ДОЛЖНО БЫТЬ НА ПАНЕЛИ НАСТРОЕК, ТИПА ТОГО, ШО КИДАЛ РУДИК, ПОЛУПРОЗРАЧНАЯ ПАНЕЛЬ, КОТОРАЯ НАХОДИТСЯ ПОВЕРХ КАРТЫ
    ПАНЕЛЬ ПОКА БУДЕТ СТАТИЧНА, УБИРАТЬСЯ ПОКА НЕ БУДЕТ, РЕАЛИЗУЕМ ЭТО ПОЗЖЕ
*/

/*

изменение границ, путешествие по миру 
    (шо-нибудь сделать с местом, которое не входит в указанные границы; 
    может быть, возможность вкл/выкл выход за границы)

(для радиуса кругов для метода взвешенных расстояний)

*/

/*
    {
        "points": [],
        "years": {
            "month": [
                
            ]
        }
    }
*/