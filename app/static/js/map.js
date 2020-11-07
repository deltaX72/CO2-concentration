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

var pointsJSON = null

//=====================================================================

const 
    southWest = L.latLng(-90, -180), 
    northEast = L.latLng(90, 200),
    bounds = L.latLngBounds(southWest, northEast),

    MIN_CON_VALUE = 380,
    MAX_CON_VALUE = 410

//=====================================================================

var map = L.map('mapid', {zoomControl: true}).setView(bounds.getCenter(), 3)
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
    current_date = $("input#date_from").val()

    $.ajax({
        url: "/handle",
        type: "get",
        data: 
            "&minimal_latitude=" + south + "&maximal_latitude=" + north +
            "&minimal_longitude=" + west + "&maximal_longitude=" + east +
            "&date_from=" + date_from + "&date_to=" + date_to
        ,
        dataType: "json",
        success: function(data) {
            pointsJSON = data
            loadAndRenderMap(map, current_date)
        },
        error: function(xhr) {
            alert('not stonks!')
        }
    })
    return false
})

$("#next").click(function() {
    if (current_date == date_to) current_date = date_from
    else {
        date = current_date.split("-")
        date[1] = parseInt(date[1]) + 1
        if (parseInt(date[1]) > 12) {
            date[0] = parseInt(date[0]) + 1
            date[1] = 1
        }
        current_date = date[0].toString() + "-" + ((date[1] < 10) ? ("0" + date[1]) : date[1]) + "-" + date[2]
    }
    loadAndRenderMap(map, current_date)
})

$("#prev").click(function() {
    if (current_date == date_from) current_date = date_to
    else {
        date = current_date.split("-")
        date[1] = parseInt(date[1]) - 1
        if (parseInt(date[1]) < 1) {
            date[0] = parseInt(date[0]) - 1
            date[1] = 12
        }
        current_date = date[0].toString() + "-" + ((date[1] < 10) ? ("0" + date[1]) : date[1]) + "-" + date[2]
    }
    loadAndRenderMap(map, current_date)
})

function loadAndRenderMap(map, date) {
    if (layer != null)      map.removeLayer(layer)
    if (borders != null)    map.removeLayer(borders)

    _date = date.split("-")
    _date[1] = parseInt(_date[1]).toString()
    // console.log(_date)

    layer = L.idwLayer(pointsJSON['periods'][_date[0]][_date[1]]['data'], {
        opacity: 0.3,
        cellSize: 8,
        exp: 2,
        // max: pointsJSON['periods'][_date[0]][_date[1]]['max'] - pointsJSON['periods'][_date[0]][_date[1]]['min'],
        max: 410 - 370,
        gradient: { 0.0: 'blue', 0.25: 'cyan', 0.5: 'lime', 0.75: 'yellow', 1: 'red' }
    })

    layer.addTo(map)

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
    console.log(current_date)
}

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