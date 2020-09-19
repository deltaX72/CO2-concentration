from app import db
from app.models import Info
from data.actions.converter import convert
import os
import time

def delete_database(db_name):
    try:
        db.session.query(db_name).delete()
        db.session.commit()
    except:
        db.session.rollback()

# db - variable which gets an access to the database (file '/app/__init__.py')
# path - path to file with gotten data from a satellite (directory: os.getcwd() + '/data/files/')
def load_data_into_database(db = db, path):
    data = convert(path)
    length = len(data)

    print('Enter required successful insertions: ', end='')
    while True:
        req_insert = int(input())
        if req_insert < 1 or req_insert > length:
            print(f'It must be in interval from 1 to {length}!')
        else: break
    
    index = 0
    successful = 0

    print(f'Inserting into database has been started!')
    last_time = time.time_ns()
    for d in data:
        info = Info(date=d[0], time=d[1], lat=float(d[2]), lon=float(d[3]), con=float(d[4]))
        if db.session.query(Info.id).filter_by(date=info.date, time=info.time, lat=info.lat, lon=info.lon, con=info.con).scalar() is None:
            db.session.add(info)
            db.session.commit()
            successful += 1
            print(successful)
        else:
            index += 1
        if successful >= req:
            break
        
    print(f'Inserting into database has been completed! Total: {length}, inserted now: {successful}, inserted before: {index}, time left: {time.time_ns() - last_time}')