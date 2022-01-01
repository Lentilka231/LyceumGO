from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import login_required,current_user
from .models import *
from . import db
import json
import datetime

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
            if request.form["submit_button"]=="ENDOFTEST":
                time=datetime.datetime.now()
                a=2
                b=365
                x=int(time.strftime("%j"))-current_user.NlastDayActiv
                x=a-b
                if x<0:
                    maxday= 366 if IsLeapYear(time.year) else 365
                    x=current_user.NlastDayActiv+int(time.strftime("%j"))-maxday
                    x=a+b-maxday
                print(x)
                if x>6:
                    current_user.Nactivity="F/F/F/F/F/F/F"
                else:
                    activity=current_user.Nactivity.split("/")
                    for i in range(x):
                        del activity[0]
                        activity.append("F")
                    current_user.Nactivity="/".join(activity)
                activity[-1]="T"
                current_user.NlastDayActiv=int(time.strftime("%j"))
                print(current_user.Nactivity)
                db.session.commit()
        with open("website/tests/NJ1.json", encoding="utf-8") as f:
            NJ = json.load(f)
        return render_template("subjects/germany.html",user=current_user,NJ1=NJ)
    return redirect(url_for("views.home"))