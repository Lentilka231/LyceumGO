from . import db
from flask_login import UserMixin
class Math (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progress1=db.Column(db.String(10))
    tests1=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Physic (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progress1=db.Column(db.String(10))
    tests1=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Informatics (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progress1=db.Column(db.String(10))
    tests1=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Programming (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progress1=db.Column(db.String(10))
    tests1=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Germany (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    progress1=db.Column(db.String(10))
    tests1=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Users (db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))
    classroom = db.Column(db.String(20))
    classroomid = db.Column(db.Integer,db.ForeignKey("classrooms.id"))
    person=db.Column(db.String(1))
    notes = db.Column(db.String(500))
    grate = db.Column(db.Integer)
    beginning = db.Column(db.Integer)
    favouritesub =db.Column(db.String(30))
    subclass = db.relationship("SubClass")
    messages = db.relationship("Messages")
    
class SubClass(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    teacher=db.Column(db.String(20))
    classroom=db.Column(db.String(20))
    subject=db.Column(db.String(10))
    progres=db.Column(db.String(1000))
    teacherid = db.Column(db.Integer, db.ForeignKey('users.id'))
  
class Classrooms (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    name = db.Column(db.String(20), unique=True)
    teacher =db.Column(db.String(30))
    numofstudents = db.Column(db.Integer)
    code = db.Column(db.String(6))
    grate = db.Column(db.Integer)
    beginning = db.Column(db.Integer)
    students = db.relationship("Users")
    # teachers=db.Column(db.String(200))

class Messages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.Integer,db.ForeignKey("users.id"))
    sender = db.Column(db.Integer)
    title = db.Column(db.String(100))
    message = db.Column(db.String(10000))
    datum = db.Column(db.String(50))
    seen = db.Column(db.Boolean)
    answer = db.Column(db.String(20))
    question = db.Column(db.String(20))