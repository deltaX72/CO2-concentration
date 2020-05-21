from app import db
from app.models import Info
import os

def convert_to_json(path_to_file):
    data = Info.query.all()

    out = '['

    for d in data:
        out += '\n\t{"date": "' + d.date + '", "time": "' + d.time + '", "lat": "' + str(d.lat) + '", "lon": "' + str(d.lon) + '", "con": "' + str(d.con) + '"},'
    file = open(path_to_file, 'w')
    if len(out) != 1:
        out = out[:len(out) - 1] + '\n]'
    else:
        out += '\n\t\n]'
    file.write(out)
    file.close()

convert_to_json(os.getcwd() + '/data/data.json')