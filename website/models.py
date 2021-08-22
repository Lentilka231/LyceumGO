from . import db
from flask_login import UserMixin

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
class Math (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progres=db.Column(db.String(10))
    tests=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favourite = db.Column(db.Boolean)

class Physic (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progres=db.Column(db.String(10))
    tests=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favourite = db.Column(db.Boolean)

class Informatics (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progres=db.Column(db.String(10))
    tests=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favourite = db.Column(db.Boolean)

class Programming (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progres=db.Column(db.String(10))
    tests=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favourite = db.Column(db.Boolean)

class User (db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))
    notes = db.relationship("Notes")
    grate = db.Column(db.Integer)
    achievements = db.Column(db.String(200))
    classroom = db.Column(db.String(50))
    beginning = db.Column(db.Integer)
    math = db.relationship("Math")
    physic = db.relationship("Physic")
    informatics = db.relationship("Informatics")
    programming = db.relationship("Programming")


class Classroom (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    teacher = db.Column(db.String(50))
    students = db.Column(db.String(100))