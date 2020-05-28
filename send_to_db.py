from app import db
from app.models import Info
from data.actions.converter import convert
import os
import time

def send(dirname):
    data = convert(dirname)
    length = len(data)
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

            # value = int(successful / length * 100)
            # if value / 10 == 0:
            #     tm = time.time_ns()
            #     print(f'Completed: {value}%, time passed: {tm - last_time}')
        
    print(f'Inserting into database has been completed! Total: {length}, inserted: {successful}')

send(os.getcwd() + '/data/files/')