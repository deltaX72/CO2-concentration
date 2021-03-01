from flask import render_template, jsonify, request
from app import app
from app.forms import InputDataForm
import json
import os
# from delaunay import delaunay
from log import log
from actions import get_dict_with_data
import pymysql
import os

dict_with_data = {
    "years": {}
}

@app.route('/')
@app.route('/index')
def index():
    form = InputDataForm()
    return render_template('first.html', form=form)

@app.route('/handle', methods=['GET', 'POST'])
def handle():
    # return convert_to_json(request_data_from_base('app1.db'))
    connection = pymysql.connections.Connection("localhost", "deltaX72", "mypassword", "co2_concentration")
    # connection = pymysql.connections.Connection(os.environ.get("DATABASE_URL"))
    log('Connected to database!')

    cur = connection.cursor()

    query_string = 'SELECT * FROM info WHERE date BETWEEN \'{}\' AND \'{}\' AND latitude BETWEEN {} AND {} AND longitude BETWEEN {} AND {};'\
    .format(
        request.args.get('date_from'), 
        request.args.get('date_to'), 
        request.args.get('minimal_latitude'), 
        request.args.get('maximal_latitude'), 
        request.args.get('minimal_longitude'), 
        request.args.get('maximal_longitude')
    )
    cur.execute(query_string)

    data = cur.fetchall()
    
    connection.close()
    log('Disconnected from database!')
    # print(data)
    
    _data = get_dict_with_data(data)
    return jsonify(_data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=5000)

# trash

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