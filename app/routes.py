from flask import render_template, request, jsonify
from app import app
from app.forms import InputDataForm
import sqlite3
import json
from read_db import convert_to_json, get_pair_of_coordinates, convert_coords_to_json
import os
from delaunay import delaunay
import drawTriangles

@app.route('/')
@app.route('/index')
def index():
    form = InputDataForm()
    return render_template('index.html', form=form)

@app.route('/handle', methods=['GET', 'POST'])
def handle():
    minimal_latitude = request.args.get('minimal_latitude')
    maximal_latitude = request.args.get('maximal_latitude')
    minimal_longitude = request.args.get('minimal_longitude')
    maximal_longitude = request.args.get('maximal_longitude')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    connection = sqlite3.connect('app.db')
    print('Connected to SQLite!')

    cur = connection.cursor()

    query_string = 'SELECT * FROM info WHERE date >= \'{}\' AND date <= \'{}\' AND lat >= {} AND lat <= {} AND lon >= {} AND lon <= {};'\
        .format(date_from, date_to, minimal_latitude, maximal_latitude, minimal_longitude, maximal_longitude)
    cur.execute(query_string)

    rows = cur.fetchall()

    response = '[\n'
    response += convert_to_json(rows)

    lat_lon = get_pair_of_coordinates(rows)
    result = delaunay(lat_lon)

    response += ',' + convert_coords_to_json(result)
    response += '\n]'

    # for i in range(len(result)):
    #     print(i)
    #     print(result[i][0])
    #     print(result[i][2])
    #     print(result[i][1])
    #     print()

    connection.close()

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)