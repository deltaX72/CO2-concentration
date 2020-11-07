from app import db
from app.models import Info
import os
import time
from log import log
import sqlite3
from flask import jsonify, request

MINIMAL_CONCENTRATION = 370

def delete_database(db_name):
    try:
        db.session.query(db_name).delete()
        db.session.commit()
    except:
        db.session.rollback()

# db - variable which gets an access to the database (file '/app/__init__.py')
# path - path to file with gotten data from a satellite (directory: os.getcwd() + '/data/files/')
def load_data_into_base(db, path):
    data = convert(path)
    length = len(data)

    print('Enter required successful insertions: ', end='')
    while True:
        req_insert = int(input())
        log(req_insert)
        if req_insert < 1 or req_insert > length:
            print(f'It must be in interval from 1 to {length}!')
        else: 
            break
    
    index = 0
    successful = 0

    log(f'Inserting into database has been started!')
    last_time = time.time_ns()
    for d in data:
        info = Info(date=d[0], time=d[1], lat=float(d[2]), lon=float(d[3]), con=float(d[4]))
        if db.session.query(Info.id).filter_by(date=info.date, time=info.time, lat=info.lat, lon=info.lon, con=info.con).scalar() is None:
            db.session.add(info)
            db.session.commit()
            successful += 1
            # log(successful)
        else:
            index += 1
        if successful >= req:
            break
        
    log(f'Inserting into database has been completed! Total: {length}, inserted now: {successful}, inserted before: {index}, time: {time.time_ns() - last_time}')

# converters

def convert(dirname):
    data = []
    for f in os.listdir(dirname):
        with open(dirname + f, 'r') as file:
            for line in file:
                string = line.split()
                data.append(string)
    return data

def request_data_from_base(db_name: str):
    connection = sqlite3.connect(db_name)
    log('Connected to database!')

    cur = connection.cursor()

    query_string = 'SELECT * FROM info WHERE date >= \'{}\' AND date <= \'{}\' AND lat >= {} AND lat <= {} AND lon >= {} AND lon <= {};'\
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
    
    return data

def convert_to_json(data):
    dictionary = {"periods": {}}
    min = 0
    max = 1000
    for d in data:
        date = d[1].split('-')
        date[1] = int(date[1])
        if date[0] not in dictionary['periods']:
            dictionary['periods'][date[0]] = {}
        if date[1] not in dictionary['periods'][date[0]]:
            dictionary['periods'][date[0]][date[1]] = {'data': []}
            dictionary['periods'][date[0]][date[1]]['min'] = 1000
            dictionary['periods'][date[0]][date[1]]['max'] = 0
        
        dictionary['periods'][date[0]][date[1]]['data'].append([d[3], d[4], d[5]])
        last = len(dictionary['periods'][date[0]][date[1]]['data']) - 1
        
        if dictionary['periods'][date[0]][date[1]]['data'][last][2] < dictionary['periods'][date[0]][date[1]]['min']:
            dictionary['periods'][date[0]][date[1]]['min'] = dictionary['periods'][date[0]][date[1]]['data'][last][2]
        
        if dictionary['periods'][date[0]][date[1]]['data'][last][2] > dictionary['periods'][date[0]][date[1]]['max']:
            dictionary['periods'][date[0]][date[1]]['max'] = dictionary['periods'][date[0]][date[1]]['data'][last][2]

    for year in dictionary['periods']:
        for month in dictionary['periods'][year]:
            for index in range(len(dictionary['periods'][year][month]['data'])):
                # dictionary['periods'][year][month]['data'][index][2] -= dictionary['periods'][year][month]['min']
                dictionary['periods'][year][month]['data'][index][2] -= MINIMAL_CONCENTRATION
    
    return jsonify(dictionary)