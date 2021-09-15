from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    tel_number = db.Column(db.String(150))
    town = db.Column(db.String(150))
    street = db.Column(db.String(150))
    psc = db.Column(db.String(150))
    status = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bring = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    label = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(150))
    color = db.Column(db.String(150))
    size = db.Column(db.String(150))
    price = db.Column(db.String(150))
    status = db.Column(db.Boolean, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)