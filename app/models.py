from app import db

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(), index=True, unique=True, nullable=False)
    latitude = db.Column(db.Float, index=True, unique=True, nullable=False)
    longitude = db.Column(db.Float, index=True, unique=True, nullable=False)
    concentration = db.Column(db.Float, index=True, unique=True, nullable=False)

    def __repr__(self):
        return f'datetime={self.datetime}, lat={self.latitude}, lon={self.longitude}, concentration={self.concentration}'