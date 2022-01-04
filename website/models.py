from . import db
from flask_login import UserMixin

class Users (db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))
    classroom = db.Column(db.String(20))
    classroomid = db.Column(db.Integer,db.ForeignKey("classrooms.id"))
    person=db.Column(db.String(1))
    notes = db.Column(db.String(500))
    beginning = db.Column(db.Integer)
    favouritesub =db.Column(db.String(30))
    messages = db.relationship("Messages")
    Ntests = db.relationship("NTests")
    INFtests = db.relationship("INFTests")
    PRGtests = db.relationship("PRGTests")
    Nactivity = db.Column(db.String(50))
    INFactivity = db.Column(db.String(50))
    PRGactivity = db.Column(db.String(50))
    NLastActivTime = db.Column(db.String(11))
    INFLastActivTime = db.Column(db.String(11))
    PRGLastActivTime = db.Column(db.String(11))
    Nprogress= db.Column(db.Integer)
    INFprogress=db.Column(db.Integer)
    PRGprogress=db.Column(db.Integer)

class Classrooms (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    name = db.Column(db.String(20), unique=True)
    teacher =db.Column(db.String(30))
    numofstudents = db.Column(db.Integer)
    code = db.Column(db.String(6))
    grade = db.Column(db.Integer)
    beginning = db.Column(db.Integer)
    students = db.relationship("Users")

class Messages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.Integer,db.ForeignKey("users.id"))
    sender = db.Column(db.Integer)
    message = db.Column(db.String(10000))
    datum = db.Column(db.String(50))
    typeM =db.Column(db.String(10))
class NTests (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    user_id =db.Column(db.Integer,db.ForeignKey("users.id"))
    result=db.Column(db.Integer)
class INFTests (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    user_id =db.Column(db.Integer,db.ForeignKey("users.id"))
    result=db.Column(db.Integer)
class PRGTests (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    user_id =db.Column(db.Integer,db.ForeignKey("users.id"))
    result=db.Column(db.Integer)