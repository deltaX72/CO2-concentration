from app import db
import sqlite3
import datetime

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True, nullable=False)
    time = db.Column(db.String(15), index=True, nullable=False)
    lat = db.Column(db.Float, index=True, nullable=False)
    lon = db.Column(db.Float, index=True, nullable=False)
    con = db.Column(db.Float, index=True, nullable=False)

    def __repr__(self):
        return ('date={}, time={}, lat={}, lon={}, con={}').format(self.date, self.time, self.lat, self.lon, self.con)