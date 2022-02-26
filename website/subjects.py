from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import login_required,current_user
from .models import *
from . import db
import json
from datetime import datetime,date

subjects = Blueprint("subjects", __name__)
def Test(sub,test):
    with open(f"{{sub}}.json") as f:
        data = json.load(f)
    return data[test]
def NJf (rocnik,kapitola):
    pass
def IsLeapYear(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
#------------INFORMATIKA-----------------------------------------------------------------------------------------------------------------------

@subjects.route("/Informatics")
def Informatika():
    return render_template("subjects/informatika.html",user=current_user)
#------------PROGRAMOVÁNÍ-----------------------------------------------------------------------------------------------------------------------
@subjects.route("/Programming")
def Programovani():
    return render_template("subjects/programovani.html",user=current_user)
#------------NĚMČINA----------------------------------------------------------------------------------------------------------------------------
@subjects.route("/Germany",methods=["GET","POST"])
def Nemcina():
    if current_user.is_authenticated:
        if request.method=="POST":
            if current_user.person=="t":
                if request.form["submit_button"]=="ENDOFTEST":
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
                        activity[-1]="T"
                        current_user.Nactivity="/".join(activity)
                    current_user.NLastActivTime=time.strftime("%Y-%m-%d")
                    Notexists=True
                    for i in range(len(current_user.Ntests)):
                        x=current_user.Ntests[i]
                        if x.name==request.form["nameOfTest"]:
                            if x.result<int(request.form["value"]):
                                x.result=int(request.form["value"])
                            Notexists=False
                    if Notexists:
                        db.session.add(NTests(name=request.form["nameOfTest"],user_id=current_user.id,result=request.form["value"]))
                    db.session.commit()
                elif request.form["submit_button"]=="SAVETEST":
                    newTest = Tests(name=request.form.get("name"),data=request.form.get("value"),creator=current_user.id)
                    db.session.add(newTest)
                    db.session.commit()
                elif request.form["submit_button"]=="REMOVETEST":
                    for i in current_user.tests:
                        if str(i.id)==request.form.get("idtest"):
                            db.session.delete(i)
                            db.session.commit()
                            break
        with open("website/tests/NJW.json", encoding="utf-8") as f:
            NJ = json.load(f)
        return render_template("subjects/germany.html",user=current_user,NJW=NJ)
    return redirect(url_for("views.index"))