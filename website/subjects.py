from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import login_required,current_user
from .models import User,Notes,Math,Physic,Informatics,Programming
from . import db
subjects = Blueprint("subjects", __name__)


@subjects.route("/Matematika")
def Matika():

    return render_template("subjects/matika.html",user=current_user,subject=Math.query.filter_by(user_id=current_user.id).first())

@subjects.route("/Fyzika")
def Fyzika():
    return render_template("subjects/fyzika.html",user=current_user,subject=Physic.query.filter_by(user_id=current_user.id).first())

@subjects.route("/Informatika")
def Informatika():
    return render_template("subjects/informatika.html",user=current_user,subject=Informatics.query.filter_by(user_id=current_user.id).first())

@subjects.route("/Programování")
def Programovani():
    return render_template("subjects/programovani.html",user=current_user,subject=Programming.query.filter_by(user_id=current_user.id).first())