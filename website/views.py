from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import current_user
from .models import *
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField,validators,Form
from wtforms.validators import InputRequired,Length,Email,EqualTo
from . import db
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
    email = StringField("Email", [validators.InputRequired(),validators.Email()])
    name = StringField("Name", [validators.InputRequired(), validators.Length(5,20)])
    password1 = PasswordField("Password1", [validators.InputRequired(), validators.Length(5,24),validators.EqualTo("password2")])
    password2 = PasswordField("Password2")
    person = SelectField("Person",choices=[("s","student"),("t","teacher")])
    submit = SubmitField("Log In")
class LoginForm(FlaskForm):
    email = StringField("Email", [validators.InputRequired(), validators.Length(5,64),validators.Email()])
    password = PasswordField("Password", [validators.InputRequired(), validators.Length(5,24)])
    submit = SubmitField("Log In")

@views.route("/",methods=["GET","POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("views.profile"))
    formL = LoginForm()
    formR = RegisterForm()
           
    if formL.validate_on_submit():
        user = Users.query.filter_by(email=formL.email.data).first()
        if user:
            if check_password_hash(user.password, formL.password.data):
                login_user(user)
                return redirect (url_for("views.profile"))
            else:
                flash("??patn?? heslo")
        else:
            flash("Email neexistuje")
    if formR.validate_on_submit():
        usere = Users.query.filter_by(email=formR.email.data).first()
        usern=False
        if formR.person.data=="t":
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
                flash("Pros??m pou???? jin?? jm??no")
        else:
            flash("Pros??m pou???? j??n?? email")
    return render_template("index.html", user=current_user,formL=formL,formR=formR)

@views.route("/profile",methods=["GET","POST"])
def profile():
    if current_user.is_authenticated:
        if request.method=="POST":
            if request.form["submit_button"]=="save":
                current_user.notes= request.form.get("note")
                current_user.favouritesub=request.form.get("FS")
                db.session.commit()
        time=datetime.now()
        y=current_user.NLastActivTime.split("-")
        x=(date(int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%d")))-date(int(y[0]),int(y[1]),int(y[2]))).days
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
        return render_template("profile.html",user=current_user,NJ=current_user.Nprogress,INF=current_user.INFprogress,PRG=current_user.PRGprogress)
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
        CTests=[]
        x=""
        if request.method=="POST":
            if request.form["submit_button"]=="findclass":
                code=request.form.get("code")
                classroom=Classrooms.query.filter_by(code=code).first()
                if classroom:
                    teacher=Users.query.filter_by(name=classroom.teacher).first()
                    createmessage(f"{current_user.name} ????d?? o p??ipojen?? do t????dy {classroom.name}. Chcete ho p????jmout?",teacher.id,"AnoNe","InviteToClassroom")
                    flash("????dost byla odesl??na")
                else:
                    flash("??patn?? code")
            elif request.form["submit_button"]=="createclass":
                fc =Classrooms.query.filter_by(name=request.form.get("name")).first()
                if not fc :
                    new_class = Classrooms(name=request.form.get("name"),teacher=current_user.name,code=createrandomcode(),beginning=date.today().year,numofstudents=0,active=True)
                    current_user.classroom=request.form.get("name")
                    db.session.add(new_class)
                    db.session.commit()
                    classroom =Classrooms.query.filter_by(name=current_user.classroom).first()
                else:
                    flash("Pros??m pou???? jin?? jm??no")
            elif request.form["submit_button"]=="deleteCLASS":
                if classroom:
                    if current_user.name==classroom.teacher:
                        for i in classroom.students:
                            i.classroom=""
                            i.classroomid=""
                        for i in classroom.scheduledtests:
                            for x in i.results:
                                db.session.delete(x)
                            db.session.delete(i)
                        db.session.delete(classroom)
                        db.session.commit()
        if classroom:
            x=enumerate(classroom.scheduledtests)
            tests=classroom.scheduledtests
            now=datetime.now()
            for i in tests:
                start=datetime(int(i.datum[:4]),int(i.datum[5:7]),int(i.datum[8:10]),int(i.datum[11:13]),int(i.datum[14:]))
                if str(current_user.id) in i.completed.split("/"):
                    CTests.append("F")
                else:
                    CTests.append("T")
                if (now-start).seconds>0:
                    i.canstart="T"
                if (now-start).seconds>i.duration*60:
                    i.canstart="E"
            if request.method=="POST":
                if request.form["submit_button"]=="newTeacher":
                    teacher = Users.query.filter_by(name=request.form.get("GermanTeacher")).first()
                    if teacher and current_user.person=="t" and teacher.person=="t":
                        createmessage(f"Pot??ebujeme t?? jako u??itele n??m??iny pro t??idu {classroom.name}", teacher.id,typeM="AnoNe",typeQ="InviteToAJob")                 
                elif "kickstudent" in request.form["submit_button"]:
                    a=request.form.get("submit_button")
                    student=Users.query.filter_by(id=a[a.find("-")+1:]).first()
                    classroom.numofstudents-=1
                    student.classroom=None
                    student.classroomid=None
                    createmessage(f"Byl jste vyhozen ze t????dy {current_user.classroom}",student.id)    
                elif "testincoming" in request.form["submit_button"]:
                    if current_user.person=="s":
                        return redirect(url_for("views.test",scheduledTest=request.form['submit_button'][12:]))
                elif "results" in request.form["submit_button"]:
                    return redirect(url_for("views.results",results=request.form["submit_button"][7:]))
            db.session.commit()
            if classroom.students:
                students=enumerate(classroom.students)
        return render_template("classroom.html",user=current_user,classroom=classroom,students=students,CT=CTests,tests=x)
    else:
        return redirect(url_for("views.index"))

@views.route("/classrooms",methods=["GET","POST"])
def classrooms():
    if current_user.is_authenticated:
        if current_user.person=="t":
            if request.method=="POST":
                a=request.form["submit_button"].split("/")
                classroom=Classrooms.query.filter_by(name=a[1]).first()
                if "results" in request.form["submit_button"]:
                    print(a[1])
                    return redirect(url_for("views.results",results=a[1]))
                if classroom.germanteacher==current_user.name:
                    if a[0]=="add":
                        if request.form.get("duration") and request.form.get("date"):
                            tests = current_user.tests
                            test=""
                            for i in tests:
                                if i.name==request.form.get("test"):
                                    test=i.id
                            if test:
                                newTest=Scheduledtests(
                                    classroom=classroom.id,
                                    duration=request.form.get("duration"),
                                    datum=request.form.get("date"),
                                    testname=request.form.get("test"),
                                    testid=test,
                                    info=request.form.get("info"),
                                    canstart="F",
                                    completed="/",
                                    creatorid=current_user.id
                                    )
                                db.session.add(newTest)
                                db.session.commit()
                    elif a[0]=="cancel":
                        scheduledTest =Scheduledtests.query.filter_by(id=a[2]).first() 
                        if scheduledTest:
                            x = Resultsfromtests.query.filter_by(scheduledTest=a[2]).all()
                            for i in x:
                                db.session.delete(i)
                            db.session.delete(scheduledTest)
                            db.session.commit()
                students=enumerate(classroom.students)
                now=datetime.now()
                CTests=[]
                tests=enumerate(classroom.scheduledtests)
                for i in classroom.scheduledtests:
                    start=datetime(int(i.datum[:4]),int(i.datum[5:7]),int(i.datum[8:10]),int(i.datum[11:13]),int(i.datum[14:]))
                    if str(current_user.id) in i.completed.split("/"):
                        CTests.append("F")
                    else:
                        CTests.append("T")
                    if (now-start).seconds>0:
                        i.canstart="T"
                    if (now-start).seconds>i.duration*60:
                        i.canstart="E"
                return render_template("classrooms.html",user=current_user,classroom=classroom,students=students,CT=CTests,tests=tests)
            x=Classrooms.query.filter_by(germanteacher=current_user.name).all()
            
            return render_template("classrooms.html",user=current_user,classrooms=x) 
        return redirect(url_for("views.profile"))
    return redirect(url_for("views.index"))

@views.route("/test/<int:scheduledTest>",methods=["GET","POST"])
def test(scheduledTest):
    if current_user.is_authenticated:
        if current_user.person=="s":
            print(request.method)
            st=Scheduledtests.query.filter_by(id=scheduledTest).first()
            if request.method=="POST":
                db.session.add(Resultsfromtests(data=request.form.get("data"),student=current_user.id,scheduledTest=scheduledTest))
                st.completed+="/"+str(current_user.id)
                db.session.commit()
                return
            now=datetime.now()
            start=datetime(int(st.datum[:4]),int(st.datum[5:7]),int(st.datum[8:10]),int(st.datum[11:13]),int(st.datum[14:]))
            duration=st.duration*60-(now-start).seconds
            for i in Classrooms.query.filter_by(name=current_user.classroom).first().scheduledtests:
                if i.id==scheduledTest and i.canstart=="T" and not(str(current_user.id) in i.completed.split("/")):
                    return render_template("test.html",user=current_user,test=Tests.query.filter_by(id=i.testid).first(),testid=scheduledTest,duration=duration)
        return redirect(url_for("views.profile"))
    return redirect(url_for("views.index"))
@views.route("/results/<int:results>",methods=["GET","POST"])
def results(results):
    if current_user.is_authenticated:
        if current_user.person=="t":
            answers = Resultsfromtests.query.filter_by(scheduledTest=results).all()
            if request.method=="POST":
                if request.form["submit_button"]=="delete":
                    test=Scheduledtests.query.filter_by(id=results).first()
                    if test.creatorid==current_user.id:
                        db.session.delete(test)
                        for i in answers:
                            db.session.delete(i)
                        db.session.commit()
                        return redirect(url_for("views.profile"))
            
            x=[]
            y=[]
            for z,m in enumerate(answers):
                x.append([])
                name=Users.query.filter_by(id=m.student).first().name
                y.append(name)
                for v,i in enumerate(m.data.split("$")):
                    x[z].append([])
                    for p,k in enumerate(i.split(";")):
                        x[z][v].append(k)
                x[-1].append(name)
                print(x)
            return render_template("results.html",user=current_user,results=answers,a=x,s=y)
        if current_user.person=="s":
            answers = Resultsfromtests.query.filter_by(student=current_user.id,scheduledTest=results).first()
            if answers:
                x=[]
                for v,i in enumerate(answers.data.split("$",answers.data.count("$"))):
                    x.append([])
                    for k in i.split(";"):
                        x[v].append(k)
                print(x)
                return render_template("results.html",user=current_user,results=answers,a=x)
    return redirect(url_for("views.index"))
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
                            createmessage(f"Byl/a jsi p????jmut/a do t????dy {classroom.name}.", message.sender)
                        elif task=="no":
                            createmessage(f"Byl/a jsi odm??tnut/a p??i vstupu do t????dy {classroom.name}.", message.sender)
                    elif message.typeQ=="InviteToAJob":
                        task=x[x.find("-")+1:]
                        classroom = Classrooms.query.filter_by(name=current_user.classroom).first()
                        teacher = Users.query.filter_by(id=message.sender).first()
                        if task=="yes":
                            classroom = Classrooms.query.filter_by(name=teacher.classroom).first()
                            for i in classroom.scheduledtests:
                                for y in Resultsfromtests.query.filter_by(scheduledTest=i.id).all():
                                    db.session.delete(y)
                                db.session.delete(i)
                            classroom.germanteacher=current_user.name
                            createmessage(f"U??itel/ka {teacher.name} p????jmul/a pr??ci u??itele.", message.sender)
                        elif task=="no":
                            createmessage(f"U??itel/ka {teacher.name} odm??tl/a pr??ci u??itele.", message.sender)
                    db.session.delete(message)
                    db.session.commit()
        return render_template("notification.html",user=current_user)
    else:
        return redirect(url_for("views.index"))
