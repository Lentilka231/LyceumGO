from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import current_user
from .models import *
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField,validators,Form
from wtforms.validators import InputRequired,Length,Email,EqualTo
from . import db
import os
import random
import string
from datetime import date,datetime
from validate_email import validate_email
from .sendmail import *

views = Blueprint("views", __name__)

subjectspro={"informatics":"0/1","programming":"0/1"}

SUBJECTS = ["Programování","Informatika","Němčina 1","Fyzika"]
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
class RegisterForm(FlaskForm):
    email = StringField("Email", [validators.InputRequired(message="Email potřebuji"), validators.Length(5,64, message="velikost majliku musí být od 5 do 64 znaků"),validators.Email(message="Zadáváš mi špatný email")])
    name = StringField("Name", [validators.InputRequired(message="Email potřebuji"), validators.Length(5,20,message="velikost jména musí být od 5 do 20 znaků")])
    password1 = PasswordField("Password1", [validators.InputRequired(message="Heslo potřebuji"), validators.Length(5,24),validators.EqualTo("password2",message="Hesla se musí rovnat")])
    password2 = PasswordField("Password2")
    person = SelectField("Person",choices=[("s","student"),("t","teacher")])
    submit = SubmitField("Log In")
class LoginForm(FlaskForm):
    email = StringField("Email", [validators.InputRequired(), validators.Length(5,64),validators.Email()])
    password = PasswordField("Password", [validators.InputRequired(), validators.Length(5,24)])
    rememberme = BooleanField("Remember me")
    submit = SubmitField("Log In")

@views.route("/home",methods=["GET","POST"])
@views.route("/",methods=["GET","POST"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("views.profile"))
    formL = LoginForm()
    formR = RegisterForm()

    if formL.validate_on_submit():
        user = Users.query.filter_by(email=formL.email.data).first()
        if user:
            if check_password_hash(user.password, formL.password.data):
                login_user(user, remember=formL.rememberme.data)
                return redirect (url_for("views.profile"))
            else:
                flash("Incorrect password, try again.",category="error")
        else:
            flash("Email does not exist.",category="error")
    if formR.validate_on_submit():
        usere = Users.query.filter_by(email=formR.email.data).first()
        usern = Users.query.filter_by(name=formR.name.data).first()
        if not usere :
            if not usern:
                SendMail(formR.email.data, formR.name.data, "Welcome")
                new_user = Users(email=formR.email.data,name=formR.name.data,password=generate_password_hash(formR.password1.data, method="sha256"),beginning=date.today().year,favouritesub="",person=formR.person.data,subjects="")
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                print("Account was created succesfully, welcome",formR.name.data)
                return redirect(url_for("views.home"))
            else:
                flash("Please use different name.")
        else:
            flash("Please use different email.")
    return render_template("index.html", user=current_user,formL=formL,formR=formR)

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
        return redirect(url_for("views.home"))
@views.route("/subjects",methods=["GET","POST"])
def subjects():
    if current_user.is_authenticated:
        if request.method=="POST":
            if request.form["submit_button"]=="createsub":
                x=request.form.get("subject")
                if x=="Programování":
                    pass
                elif x=="Informatika":
                    pass
                elif x=="Fyzika":
                    if not Physics.query.filter_by(user_id=current_user.id).first():
                        current_user.subjects+="Physics/"
                        news = Physics(progress="0/100",user_id=current_user.id,subname="Fyzika")
                        db.session.add(news)
                        db.session.commit()
                    else:
                        flash("Tato učebna už existuje")
                elif x=="Němčina 1":
                    if not Germany.query.filter_by(user_id=current_user.id).first():
                        current_user.subjects+="Germany1/"
                        news = Germany(progress="0/100",user_id=current_user.id,subname="Němčina 1")
                        db.session.add(news)
                        db.session.commit()
                    else:
                        flash("Tato učebna už existuje")
        usersub=[]
        for i in current_user.subjects.split("/"):
            if i=="Germany1":
                usersub.append(Germany.query.filter_by(user_id=current_user.id).first())
            elif i=="Informatics":
                usersub.append(Informatics.query.filter_by(user_id=current_user.id).first())
            elif i=="Programming":
                usersub.append(Programming.query.filter_by(user_id=current_user.id).first())
            elif i=="Physics":
                usersub.append(Physics.query.filter_by(user_id=current_user.id).first())
        return render_template("subjects.html",user=current_user,subjects=SUBJECTS,usersub=usersub)
    else:
        return redirect(url_for("views.home"))

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
                student=Users.query.filter_by(id=a[a.find("-")+1:]).first()
                classroom.numofstudents-=1
                student.classroom=None
                student.classroomid=None
                createmessage("Vyhazov", f"Byl jste vyhozen ze třídy {current_user.classroom}",student.id,"none")    
        if classroom:
            if classroom.students:
                students=enumerate(classroom.students)
        return render_template("classroom.html",user=current_user,classroom=classroom,students=students,teachers=teachers,subjects=SUBJECTS)
    else:
        return redirect(url_for("views.home"))

@views.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("views.home"))

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