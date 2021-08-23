from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import login_required,current_user
from .models import User,Notes,Math,Physic,Informatics,Programming
from . import db
import os
views = Blueprint("views", __name__)
def getSubjects():
    return {"Matika":Math.query.filter_by(user_id=current_user.id).first(),"Fyzika":Physic.query.filter_by(user_id=current_user.id).first(),"Informatika":Informatics.query.filter_by(user_id=current_user.id).first(),"Programování":Programming.query.filter_by(user_id=current_user.id).first(),}

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
            print(r)
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
            print(request.form["submit_button"])
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