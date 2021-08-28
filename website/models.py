from . import db
from flask_login import UserMixin
# Rozdělit User na Studenty a Učitele NE DOHROMADY
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
class Math (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progress1=db.Column(db.String(10))
    tests1=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favourite = db.Column(db.Boolean)

class Physic (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progress1=db.Column(db.String(10))
    tests1=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favourite = db.Column(db.Boolean)

class Informatics (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progress1=db.Column(db.String(10))
    tests1=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favourite = db.Column(db.Boolean)

class Programming (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progress1=db.Column(db.String(10))
    tests1=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favourite = db.Column(db.Boolean)

class User (db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))
    notes = db.relationship("Notes")
    person = db.Column(db.String(7))
    grate = db.Column(db.Integer)
    score = db.Column(db.Integer)
    achievements = db.Column(db.String(200))
    classroom = db.Column(db.String(20))
    beginning = db.Column(db.Integer)
    math = db.relationship("Math")
    physic = db.relationship("Physic")
    informatics = db.relationship("Informatics")
    programming = db.relationship("Programming")

class Subjects(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    teacher=db.Column(db.String(20))
    students=db.Column(db.String(100))
    
class Classroom (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    teacher = db.Column(db.String(50))
    students = db.Column(db.String(100))
    code = db.Column(db.String(6))
    grate = db.Column(db.Integer)
    beginning = db.Column(db.Integer)
    teachers=db.Column(db.String(200))

class Messages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    message = db.Column(db.String(10000))