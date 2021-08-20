from . import db
from flask_login import UserMixin

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User (db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))
    notes = db.relationship("Notes")
    grate = db.Column(db.Integer)
    favouritesubjects = db.Column(db.String(50))
    achievements = db.Column(db.String(200))
    classroom = db.Column(db.String(50))
    beginning = db.Column(db.Integer)


class Classroom (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    teacher = db.Column(db.String(50))
    students = db.Column(db.String(100))