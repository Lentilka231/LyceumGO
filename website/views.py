from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import login_required,current_user
from .models import User,Notes,Math,Physic,Informatics,Programming,Classroom,Messages
from . import db
import os
import random
import string
from datetime import date,datetime
views = Blueprint("views", __name__)
SUBJECTS =["Matematika","Fyzika","Progamování","Informatika"]

def getSubjects():
    return {"Matematika":Math.query.filter_by(user_id=current_user.id).first(),"Fyzika":Physic.query.filter_by(user_id=current_user.id).first(),"Informatika":Informatics.query.filter_by(user_id=current_user.id).first(),"Programování":Programming.query.filter_by(user_id=current_user.id).first(),}
def createrandomcode():
    x=""
    for i in range(6):
        x+=random.choice(string.ascii_letters)
    return x
def createmessage(title,message,prijemce):
    datum=str(datetime.now())[:-11]
    new_message=Messages(user_name=prijemce,title=title,message=message,datum=datum,seen=False)
    db.session.add(new_message)
    print("message was created")
    db.session.commit()
@views.route("/home")
@views.route("/")
def home():
    return render_template("index.html",user=current_user)

@views.route("/profile",methods=["GET","POST"])
def profile():
    if current_user.is_authenticated:
        subjects=getSubjects()
        note=Notes.query.filter_by(user_id=current_user.id).first()
        if request.method=="POST":
            r=request.form["submit_button"]
            if r in subjects.keys():
                if subjects[r].favourite==True:
                    print("FALSEE")
                    subjects[r].favourite=False
                else:
                    print("TRUEE")
                    subjects[r].favourite=True
        db.session.commit()

        return render_template("profile.html",user=current_user,note=note,subjects=subjects)
    else:
        return redirect(url_for("auth.login"))

@views.route("/editprofile",methods=["GET","POST"])
def editprofile():
    if current_user.is_authenticated:
        usernote=Notes.query.filter_by(id=current_user.id).first()
        subjects=getSubjects()
        if request.method=="POST":
            if request.form["submit_button"]=="Uložit":
                name = request.form.get("name")
                note = request.form.get("note")
                if name:
                    usern = User.query.filter_by(name=name).first()
                    if not usern:
                        current_user.name=name
                    else:
                        return redirect(url_for("views.editprofile"))

                usernote.data=note
                db.session.commit()
            elif request.form["submit_button"]=="Zrušit":
                pass
            elif request.form["submit_button"] in subjects.keys():
                subjects[request.form["submit_button"]].favourite=False
                db.session.commit()
                return render_template("editprofile.html",user=current_user,note=usernote,subjects=subjects)
            return redirect(url_for("views.profile"))
            
        return render_template("editprofile.html",user=current_user,note=usernote,subjects=subjects)
    else:
        return redirect(url_for("auth.login"))

@views.route("/subjects")
def subjects():
    if current_user.is_authenticated:
        subjects=[getSubjects()]
        return render_template("subjects.html",user=current_user,subjects=enumerate(subjects))
    else:
        return redirect(url_for("auth.login"))

@views.route("/classroom",methods=["GET","POST"])
def classroom():
    if current_user.is_authenticated:
        classroom=Classroom.query.filter_by(name=current_user.classroom).first()
        subjects=enumerate([getSubjects()])
        x={}
        students=[]
        teachers=User.query.filter_by(person="t").all()
        if classroom:
            for i in classroom.students.split("/"):
                students.append(User.query.filter_by(name=i))
            for i in classroom.teachers.split("/"):
                a=i.find(":")
                x[i[:a]]=i[a+1:]
        if request.method=="POST":
            if request.form["submit_button"]:
                if request.form["submit_button"]=="Odeslat":
                    code=request.form.get("code")
                    classroom=Classroom.query.filter_by(code=code).first()
                    teacher=User.query.filter_by(name=classroom.teacher).first()
                    createmessage("Žádost", f"{current_user.name} žádá o připojení do třídy {classroom.name}. Chcete ho příjmout",teacher.name)
                elif request.form["submit_button"]=="createclass":
                    fc =Classroom.query.filter_by(name=request.form.get("name")).first()
                    if not fc :
                        new_class = Classroom(name=request.form.get("name"),teacher=current_user.name,code=createrandomcode(),beginning=date.today().year,students="/"*29,teachers="/".join(i+":" for i in SUBJECTS))
                        current_user.classroom=request.form.get("name")
                        db.session.add(new_class)
                        db.session.commit()
                    else:
                        flash("použij jiné jméno")
                elif request.form["submit_button"]=="sendt":
                    t=""
        

        return render_template("classroom.html",user=current_user,classroom=classroom,students=students,teachers=teachers,subxteach=x)
    else:
        return redirect(url_for("auth.login"))

@views.route("/notification",methods=["GET","POST"])
def notification():
    if current_user.is_authenticated:
        messages=Messages.query.filter_by(user_name=current_user.name).all()
        print(messages)
        return render_template("notification.html",user=current_user,messages=messages)
    else:
        return redirect(url_for("auth.login"))