from app import db
from app.models import Info

def convert_to_json(path_to_file):
    data = Info.query.all()

    # to json
    out = '['

    for d in data:
        out += '\n\t{"date": "' + d.date + '", "time": "' + d.time + '", "lat": "' + d.lat + '", "lon": "' + d.lon + '", "con": "' + d.con + '"},'
    out = out[:len(out) - 1] + '\n]'

    with open(path_to_file) as file:
        file.write(out)
        file.close()

convert_to_json('/home/deltax72/Project CO2/data/data.json')