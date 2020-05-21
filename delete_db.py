from app import db
from app.models import Info

try:
    db.session.query(Info).delete()
    db.session.commit()
except:
    db.session.rollback()