from flask import render_template, jsonify
from app import app
from app.forms import InputDataForm
import json
import os
# from delaunay import delaunay
from log import log
from actions import request_data_from_base
from actions import convert_to_json

dict_with_data = {
    "years": {}
}

@app.route('/')
@app.route('/index')
def index():
    form = InputDataForm()
    return render_template('index.html', form=form)

@app.route('/handle', methods=['GET', 'POST'])
def handle():
    return convert_to_json(request_data_from_base('app1.db'))

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