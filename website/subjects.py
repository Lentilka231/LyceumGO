from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import login_required,current_user
from .models import User,Notes,Math,Physic,Informatics,Programming
from . import db
import json


subjects = Blueprint("subjects", __name__)
def Test(sub,test):
    with open(f"{{sub}}.json") as f:
        data = json.load(f)
    return data[test]

#------------MATEMATIKA-----------------------------------------------------------------------------------------------------------------------
@subjects.route("/Matematika")
def Matika():

    return render_template("subjects/matika.html",user=current_user,subject=Math.query.filter_by(user_id=current_user.id).first())
#------------FYZYKA-----------------------------------------------------------------------------------------------------------------------
@subjects.route("/Fyzika",methods=["GET","POST"])
def Fyzika():
    if current_user.is_authenticated:
        if request.method=="POST":
            t=request.form["test"]
            test=Test("Fyzika",t[1:])
            if t[0]=="q":
                return render_template("subjects/fyzika.html",toknow="q",test=test,user=current_user,subject=Physic.query.filter_by(user_id=current_user.id).first())
            elif t[0]=="a":
                return render_template("subjects/fyzika.html",toknow="a",test=test,user=current_user,subject=Physic.query.filter_by(user_id=current_user.id).first())
        return render_template("subjects/fyzika.html",test="",user=current_user,subject=Physic.query.filter_by(user_id=current_user.id).first())
    return redirect(url_for("auth.login"))
#------------INFORMATIKA-----------------------------------------------------------------------------------------------------------------------

@subjects.route("/Informatika")
def Informatika():
    return render_template("subjects/informatika.html",user=current_user,subject=Informatics.query.filter_by(user_id=current_user.id).first())
#------------PROGRAMOVÁNÍ-----------------------------------------------------------------------------------------------------------------------
@subjects.route("/Programování")
def Programovani():
    return render_template("subjects/programovani.html",user=current_user,subject=Programming.query.filter_by(user_id=current_user.id).first())