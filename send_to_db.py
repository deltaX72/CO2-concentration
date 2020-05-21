from app import db
from app.models import Info
from data.converter import convert

def send(dirname):
    data = convert(dirname)

    for d in data:
        print(d)
        info = Info(date=d[0], time=d[1], lat=float(d[2]), lon=float(d[3]), con=float(d[4]))
        db.session.add(info)
        db.session.commit()

send('/home/deltax72/Project CO2/data/files/')