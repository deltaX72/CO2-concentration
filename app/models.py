from app import db

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), index=True, unique=True, nullable=False)
    time = db.Column(db.String(12), index=True, unique=True, nullable=False)
    lat = db.Column(db.Float, index=True, unique=True, nullable=False)
    lon = db.Column(db.Float, index=True, unique=True, nullable=False)
    con = db.Column(db.Float, index=True, unique=True, nullable=False)

    def __repr__(self):
        return ('date={}, time={}, lat={}, lon={}, con={}').format(self.date, self.time, self.lat, self.lon, self.con)