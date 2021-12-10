from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import login_required,current_user
from .models import *
from . import db
import json


subjects = Blueprint("subjects", __name__)
def Test(sub,test):
    with open(f"{{sub}}.json") as f:
        data = json.load(f)
    return data[test]
def NJf (rocnik,kapitola):
    pass

#------------INFORMATIKA-----------------------------------------------------------------------------------------------------------------------

@subjects.route("/Informatika")
def Informatika():
    return render_template("subjects/informatika.html",user=current_user,subject=Informatics.query.filter_by(user_id=current_user.id).first())
#------------PROGRAMOVÁNÍ-----------------------------------------------------------------------------------------------------------------------
@subjects.route("/Programování")
def Programovani():
    return render_template("subjects/programovani.html",user=current_user,subject=Programming.query.filter_by(user_id=current_user.id).first())
#------------Fyzika-----------------------------------------------------------------------------------------------------------------------
@subjects.route("/Fyzika")
def Fyzika():
    return render_template("subjects/physics.html",user=current_user,subject=Physics.query.filter_by(user_id=current_user.id).first())
#------------NĚMČINA----------------------------------------------------------------------------------------------------------------------------
@subjects.route("/Němčina 1")
def Nemcina():
    subclass=None
    with open("website/tests/NJ1.json", encoding="utf-8") as f:
        NJ = json.load(f)
    if current_user.is_authenticated:
        return render_template("subjects/germany.html",user=current_user,subject=Germany.query.filter_by(user_id=current_user.id).first(),NJ1=NJ)
    return redirect(url_for("auth.login"))