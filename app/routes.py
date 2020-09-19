from flask import render_template, request, jsonify
from app import app
from app.forms import InputDataForm
import sqlite3
import json
from converters import get_pair_of_coordinates
import os
# from delaunay import delaunay

dict_with_data = {
    "points": [],
    "months": {} # YYYY-MM
}

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

    connection = sqlite3.connect('app1.db')
    print('Connected to SQLite!')

    cur = connection.cursor()

    query_string = 'SELECT * FROM info WHERE date >= \'{}\' AND date <= \'{}\' AND lat >= {} AND lat <= {} AND lon >= {} AND lon <= {};'\
        .format(date_from, date_to, minimal_latitude, maximal_latitude, minimal_longitude, maximal_longitude)
    cur.execute(query_string)

    dict_with_data['points'] = cur.fetchall()
    connection.close()

    # to json

    for i in dict_with_data['points']:
        line = i[1].split('-')
        dict_with_data['months']['{}-{}'.format(line[0], line[1])] = []
    # dict_with_data['months'] = sorted(dict_with_data['months'])

    
    for i in dict_with_data['points']:
        line = i[1].split('-')
        dict_with_data['months']['{}-{}'.format(line[0], line[1])].append(i)

    # triangulation
    # empty list 'lst'
    lst = dict_with_data['months'].copy()

    for i in dict_with_data['points']:
        line = i[1].split('-')
        position = '{}-{}'.format(line[0], line[1])
        lst[position].append(i)
    
    # months = lst.keys() 
    # for i in months:
    #     pair = []
    #     key = str(i)
    #     pair = get_pair_of_coordinates(dict_with_data['months'][key])
    #     pair = list(set(pair))

    #     result = delaunay(pair)
    #     dict_with_data['months'][key] = []
    #     for triangles in result:
    #         l = []
    #         for index in range(3):
    #             for value in dict_with_data['points']:
    #                 if value[3] == triangles[index][0] and value[4] == triangles[index][1]:
    #                     l.append(value)
    #                     break
    #         dict_with_data['months'][key].append(l)
    
    return jsonify(dict_with_data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)