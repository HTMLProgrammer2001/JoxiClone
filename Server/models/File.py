from server import db
import datetime


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    extension = db.Column(db.String(10))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
