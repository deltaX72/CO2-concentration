from app import db
from app.models import Info
import os

# def convert_to_json(path_to_file):
#     data = Info.query.all()

#     out = '['

#     for d in data:
#         out += '\n\t{"date": "' + d.date + '", "time": "' + d.time + '", "lat": "' + str(d.lat) + '", "lon": "' + str(d.lon) + '", "con": "' + str(d.con) + '"},'
#     file = open(path_to_file, 'w')
#     if len(out) != 1:
#         out = out[:len(out) - 1] + '\n]'
#     else:
#         out += '\n\t\n]'
#     file.write(out)
#     file.close()

# convert_to_json(os.getcwd() + '/data/data.json')

def convert_to_json_in_file(data, path_to_file):
    if type(data) is list:
        out = '['

        for d in data:
            out += '\n\t{"date": "' + d[1] + '", "time": "' + d[2] + '", "lat": "' + str(d[3]) + '", "lon": "' + str(d[4]) + '", "con": "' + str(d[5]) + '"},'
        file = open(path_to_file, 'w')
        if len(out) != 1:
            out = out[:len(out) - 1] + '\n]'
        else:
            out += '\n\t\n]'
        file.write(out)
        file.close()
        return 
    return None

def convert_to_json(data):
    out = '['
    for d in data:
        out += '\n\t{"date": "' + d[1] + '", "time": "' + d[2] + '", "lat": "' + str(d[3]) + '", "lon": "' + str(d[4]) + '", "con": "' + str(d[5]) + '"},'
    if len(out) != 1:
        out = out[:len(out) - 1] + '\n]'
    else:
        out += '\n\t\n]'
    return out

# convert_to_json_in_file(os.getcwd() + '/data/data.json')