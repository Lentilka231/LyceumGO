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
def createrandomcode():
    x=""
    for i in range(6):
        x+=random.choice(string.ascii_letters)
    return x
def createmessage(message,prijemceid,typeM="regular",typeQ="regular"):
    datum=str(datetime.now())[:-10]
    new_message=Messages(user_name=prijemceid,message=message,datum=datum,sender=current_user.id,typeM=typeM,typeQ=typeQ)
    db.session.add(new_message)
    print("message was created")
    db.session.commit()
def IsLeapYear(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
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

@views.route("/",methods=["GET","POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    formL = LoginForm()
    formR = RegisterForm()
           
    if formL.validate_on_submit():
        user = Users.query.filter_by(email=formL.email.data).first()
        if user:
            if check_password_hash(user.password, formL.password.data):
                login_user(user, remember=formL.rememberme.data)
                return redirect (url_for("views.home"))
            else:
                flash("Incorrect password, try again.",category="error")
        else:
            flash("Email does not exist.",category="error")
    if formR.validate_on_submit():
        usere = Users.query.filter_by(email=formR.email.data).first()
        usern = Users.query.filter_by(name=formR.name.data).first()
        if not usere :
            if not usern:
                new_user=Users(
                email=formR.email.data,
                name=formR.name.data,
                password=generate_password_hash(formR.password1.data, method="sha256"),
                beginning=date.today().year,
                favouritesub="",
                person=formR.person.data,
                Nactivity="F/F/F/F/F/F/F",
                INFactivity="F/F/F/F/F/F/F",
                PRGactivity="F/F/F/F/F/F/F",
                NLastActivTime=datetime.now().strftime("%Y-%m-%d"),
                INFLastActivTime=datetime.now().strftime("%Y-%m-%d"),
                PRGLastActivTime=datetime.now().strftime("%Y-%m-%d"),
                Nprogress=0,
                INFprogress=0,
                PRGprogress=0)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                SendMail(formR.email.data, formR.name.data, "Welcome")
                print("Account was created succesfully, welcome",formR.name.data)
                return redirect(url_for("views.index"))
            else:
                flash("Please use different name.")
        else:
            flash("Please use different email.")
    return render_template("index.html", user=current_user,formL=formL,formR=formR)

@views.route("/home",methods=["GET","POST"])
def home():
    if current_user.is_authenticated:
        if request.method=="POST":
            if request.form["submit_button"]=="save":
                current_user.notes= request.form.get("note")
                current_user.favouritesub=request.form.get("FS")
                db.session.commit()
        time=datetime.now()
        y=current_user.NLastActivTime.split("-")
        x=(date(int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%j")))-date(int(y[0]),int(y[1]),int(y[2]))).days
        if x>6:
            current_user.Nactivity="F/F/F/F/F/F/F"
        else:
            activity=current_user.Nactivity.split("/")
            for i in range(x):
                del activity[0]
                activity.append("F")
            current_user.Nactivity="/".join(activity)
        current_user.NLastActivTime=time.strftime("%Y-%m-%d")
        db.session.commit()
        return render_template("home.html",user=current_user,NJ=current_user.Nprogress,INF=current_user.INFprogress,PRG=current_user.PRGprogress)
    else:
        return redirect(url_for("views.index"))
@views.route("/subjects",methods=["GET","POST"])
def subjects():
    if current_user.is_authenticated:
        return render_template("subjects.html",user=current_user,)
    else:
        return redirect(url_for("views.index"))

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
                    createmessage(f"{current_user.name} žádá o připojení do třídy {classroom.name}. Chcete ho příjmout?",teacher.id,"AnoNe","InviteToClassroom")
                    flash("Žádost byla odeslána")
                else:
                    flash("Špatný code")
            elif request.form["submit_button"]=="createclass":
                fc =Classrooms.query.filter_by(name=request.form.get("name")).first()
                if not fc :
                    new_class = Classrooms(name=request.form.get("name"),teacher=current_user.name,code=createrandomcode(),beginning=date.today().year,numofstudents=0,active=True)
                    current_user.classroom=request.form.get("name")
                    db.session.add(new_class)
                    db.session.commit()
                    classroom =Classrooms.query.filter_by(name=current_user.classroom).first()
                else:
                    flash("použij jiné jméno")
            elif request.form["submit_button"]=="newTeacher":
                teacher = Users.query.filter_by(name=request.form.get("GermanTeacher")).first()
                if teacher and current_user.person=="t" and teacher.person=="t":
                    createmessage(f"Potřebujeme tě jako učitele němčiny pro třidu {classroom.name}", teacher.id,typeM="AnoNe",typeQ="InviteToAJob")                 
            elif "kickstudent" in request.form["submit_button"]:
                a=request.form.get("submit_button")
                student=Users.query.filter_by(id=a[a.find("-")+1:]).first()
                classroom.numofstudents-=1
                student.classroom=None
                student.classroomid=None
                createmessage(f"Byl jste vyhozen ze třídy {current_user.classroom}",student.id)    
        if classroom:
            if classroom.students:
                students=enumerate(classroom.students)
        return render_template("classroom.html",user=current_user,classroom=classroom,students=students,teachers=teachers)
    else:
        return redirect(url_for("views.index"))
@views.route("/classrooms",methods=["GET","POST"])
def classrooms():
    if request.method=="POST":
        if request.form["submit_button"]=="changePage" and current_user.person=="t":
            return 
    x=Classrooms.query.filter_by(germanteacher=current_user.name).all()
    return render_template("classrooms.html",user=current_user,classrooms=x) 
@views.route("/",methods=["GET","POST"])
def students():
    return render_template("students.html",user=current_user)
@views.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("views.index"))

@views.route("/notification",methods=["GET","POST"])
def notification():
    if current_user.is_authenticated:
        if request.method=="POST":
            if request.form["submit_button"]:
                x=request.form["submit_button"]
                message=""
                for mess in current_user.messages:
                    if mess.id==int(x[:x.find("-")]):
                        message=mess
                        break
                if message:
                    if message.typeQ=="InviteToClassroom":
                        task=x[x.find("-")+1:]
                        classroom = Classrooms.query.filter_by(name=current_user.classroom).first()
                        if task=="yes" and len(classroom.students)<30:
                            boy=Users.query.filter_by(id=message.sender).first()
                            boy.classroom=classroom.name
                            boy.classroomid=classroom.id
                            classroom.numofstudents+=1
                            createmessage(f"Byl/a jsi příjmut/a do třídy {classroom.name}.", message.sender)
                        elif task=="no":
                            createmessage(f"Byl/a jsi odmítnut/a při vstupu do třídy {classroom.name}.", message.sender)
                    elif message.typeQ=="InviteToAJob":
                        task=x[x.find("-")+1:]
                        classroom = Classrooms.query.filter_by(name=current_user.classroom).first()
                        teacher = Users.query.filter_by(id=message.sender).first()
                        if task=="yes":
                            classroom = Classrooms.query.filter_by(name=teacher.classroom).first()
                            classroom.germanteacher=current_user.name
                            createmessage(f"Učitel/ka {teacher.name} příjmul/a práci učitele.", message.sender)
                        elif task=="no":
                            createmessage(f"Učitel/ka {teacher.name} odmítl/a práci učitele.", message.sender)
                    db.session.delete(message)
                    db.session.commit()
        return render_template("notification.html",user=current_user)
    else:
        return redirect(url_for("auth.login"))