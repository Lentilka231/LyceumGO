from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import current_user
from .models import *
from . import db
import os
import random
import string
from datetime import date,datetime
views = Blueprint("views", __name__)
SUBJECTS = [["Fyzika","Chemie","Programování","Informatika","Němčina"]]
def createrandomcode():
    x=""
    for i in range(6):
        x+=random.choice(string.ascii_letters)
    return x
def createmessage(title,message,prijemceid,question):
    datum=str(datetime.now())[:-11]
    new_message=Messages(user_name=prijemceid,title=title,message=message,datum=datum,seen=False,answer="none",sender=current_user.id,question=question)
    db.session.add(new_message)
    print("message was created")
    db.session.commit()

def createsubforstudents(studentid,s):
    if studentid:
        if s=="Matematika":
            return Math(user_id=studentid,progress="0/100")
        elif s=="Fyzika":
            return Physic(user_id=studentid,progress="0/100")
        elif s=="Programování":
            return Programming(user_id=studentid,progress="0/100")
        elif s=="Informatika":
            return Informatics(user_id=studentid,progress="0/100")
        elif s=="Němčina":
            return Germany(user_id=studentid,progress="0/100")


@views.route("/home")
@views.route("/")
def home():
    return render_template("index.html",user=current_user)

@views.route("/profile",methods=["GET","POST"])
def profile():
    if current_user.is_authenticated:
        if current_user.favouritesub.split("/"):
            x=current_user.favouritesub.split("/")
        if request.method=="POST":
            if request.form["submit_button"]=="save":
                current_user.notes= request.form.get("note")
                db.session.commit()
            elif request.form["submit_button"]=="cancel":
                pass
            elif request.form["submit_button"]:
                if not x[0]:
                    x[0] = request.form["submit_button"]
                elif not x[1]:
                    x[1] =request.form["submit_button"]
                current_user.favouritesub=x[0]+"/"+x[1]
            db.session.commit()
        return render_template("profile.html",user=current_user,subjects={},favouritesub=x)
    else:
        return redirect(url_for("auth.login"))
@views.route("/subjects",methods=["GET","POST"])
def subjects():
    if current_user.is_authenticated:
        return render_template("subjects.html",user=current_user)
    else:
        return redirect(url_for("auth.login"))

@views.route("/classroom",methods=["GET","POST"])
def classroom():
    if current_user.is_authenticated:
        classroom=Classrooms.query.filter_by(name=current_user.classroom).first()
        students=[]

        teachers=Users.query.filter_by(person="t").all()
        if request.method=="POST":
            if request.form["submit_button"]=="findclass":
                code=request.form.get("code")
                classroom=Classrooms.query.filter_by(code=code).first()
                if classroom:
                    teacher=Users.query.filter_by(name=classroom.teacher).first()
                    createmessage("Žádost", f"{current_user.name} žádá o připojení do třídy {classroom.name}. Chcete ho příjmout",teacher.id,"anone")
                    flash("Žádost byla odeslána")
                else:
                    flash("Špatný code")
            elif request.form["submit_button"]=="createclass":
                fc =Classrooms.query.filter_by(name=request.form.get("name")).first()
                if not fc :
                    new_class = Classrooms(name=request.form.get("name"),teacher=current_user.name,code=createrandomcode(),beginning=date.today().year,numofstudents=0,active=True,grade=request.form.get("grade")[1])
                    current_user.classroom=request.form.get("name")
                    db.session.add(new_class)
                    db.session.commit()
                    classroom =Classrooms.query.filter_by(name=current_user.classroom).first()
                else:
                    flash("použij jiné jméno")
            elif request.form["submit_button"]=="sendmess":
                pass
            elif "kickstudent" in request.form["submit_button"]:
                a=request.form.get("submit_button")
                print(a,a[a.find("-")+1:])
                student=Users.query.filter_by(id=a[a.find("-")+1:]).first()
                classroom.numofstudents-=1
                student.classroom=None
                student.classroomid=None

                createmessage("Vyhazov", f"Byl jste vyhozen ze třídy {current_user.classroom}",student.id,"none")
                    
            elif request.form["submit_button"]=="createsubclass":
                a=True
                for i in classroom.subclass:
                    if request.form.get("subject")==i.subject:
                        a=False
                if a:
                    newsubclass = SubClass(teacher=request.form.get("teacher"),teacherid=current_user.id,subject=request.form.get("subject"),classroomname=classroom.name,grade=classroom.grade)
                    newgermany = Germany(progress="0/100",user_id=current_user.id)
                    db.session.add(newsubclass)
                    for student in classroom.students:
                        db.session.add(createsubforstudents(student.id, request.form.get("subject")))
                    db.session.commit()
                else:
                    flash("Tato učebna pro tuto třídu už existuje")
            elif "destroysubclass" in request.form["submit_button"]:
                a=request.form.get("submit_button")
                subclass = SubClass.query.filter_by(id=a[a.find("-")+1:]).first()
                db.session.delete(subclass)
                db.session.commit()
        if classroom:
            if classroom.students:
                students=enumerate(classroom.students)
        return render_template("classroom.html",user=current_user,classroom=classroom,students=students,teachers=teachers,subjects=SUBJECTS)
    else:
        return redirect(url_for("auth.login"))

@views.route("/notification",methods=["GET","POST"])
def notification():
    if current_user.is_authenticated:
        if request.method=="POST":
            if request.form["submit_button"]:
                x=request.form["submit_button"]
                for mess in current_user.messages:
                    if mess.id==int(x[:x.find("-")]):
                        message=mess
                        break
                task=x[x.find("-")+1:]
                message.answer=task
                message.seen=True
                classroom = Classrooms.query.filter_by(name=current_user.classroom).first()
                if task=="yes" and len(classroom.students)<30:
                    boy=Users.query.filter_by(id=message.sender).first()
                    boy.classroom=classroom.name
                    boy.classroomid=classroom.id
                    for sub in classroom.subclass:
                        db.session.add(createsubforstudents(boy.id, sub.subject))
                    classroom.numofstudents+=1
                    db.session.commit()
                    createmessage("Odpověď",f"Byl jsi příjmut do třídy {classroom.name}.", message.sender,"none")
                elif task=="no":
                    createmessage("Odpověď", f"Byl jsi odmítnut při vstupu do třídy {classroom.name}.", message.sender,"none")
                elif task=="destroy":
                    db.session.delete(message)
                    db.session.commit()
        return render_template("notification.html",user=current_user)
    else:
        return redirect(url_for("auth.login"))