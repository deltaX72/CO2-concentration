from app import db
from app.models import Info
import os

def get_pair_of_coordinates(data):
    out = []
    for i in data:
        out.append(tuple([i[3], i[4]]))
    return out

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

# def convert_to_json_in_file(data, path_to_file):
#     if type(data) is list:
#         out = '['

#         for d in data:
#             out += '\n\t{"date": "' + d[1] + '", "time": "' + d[2] + '", "lat": "' + str(d[3]) + '", "lon": "' + str(d[4]) + '", "con": "' + str(d[5]) + '"},'
#         file = open(path_to_file, 'w')
#         if len(out) != 1:
#             out = out[:len(out) - 1] + '\n]'
#         else:
#             out += '\n\t\n]'
#         file.write(out)
#         file.close()
#         return 
#     return None

# def convert_to_json(data):
#     out = '['
#     for d in data:
#         out += '\n\t{"date": "' + d[1] + '", "time": "' + d[2] + '", "lat": "' + str(d[3]) + '", "lon": "' + str(d[4]) + '", "con": "' + str(d[5]) + '"},'
#         # out += ('\n\t{"date": "{}", "time": "{}", "lat": "{}", "lon": "{}", "con": "{}"},').format(d[1], d[2], str(d[3]), str(d[4]), str(d[5]))
#     if len(out) != 1:
#         out = out[:len(out) - 1] + '\n]'
#     else:
#         out += '\n\t\n]'
#     return out

# def convert_coords_to_json(triangles):
#     out = '\n['
#     for i in range(len(triangles)):
#         out += '\n\t['
#         for index in range(3):
#             out += '\n\t\t{"lat": "' + str(triangles[i][index][0]) + '", "lon": "' + str(triangles[i][index][1]) + '"},'
#         out = out[:len(out) - 1]
#         out += '\n\t],'
#         if i == len(triangles) - 1:
#             out = out[:len(out) - 1]
#     out += '\n]'

#     return out
    

# # convert_to_json_in_file(os.getcwd() + '/data/data.json')