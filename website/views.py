from flask import Blueprint, render_template, redirect, url_for,request,flash,request
from flask_login import login_required,current_user
from .models import User,Notes
from . import db
import os
views = Blueprint("views", __name__)


@views.route("/home")
@views.route("/")
def home():
    return render_template("index.html",user=current_user)

@views.route("/profile")
def profile():
    if current_user.is_authenticated:
        note=Notes.query.filter_by(user_id=current_user.id).first()
        return render_template("profile.html",user=current_user,note=note,favouritesubjects=[x for x in current_user.favouritesubjects.split("/")])
    else:
        return redirect(url_for("auth.login"))

@views.route("/editprofile",methods=["GET","POST"])
def editprofile():
    if current_user.is_authenticated:
        usernote=Notes.query.filter_by(id=current_user.id).first()
        fs=[x for x in current_user.favouritesubjects.split("/")]
        if "" in fs:
            fs.remove("")
        if request.method=="POST":
            if request.form["submit_button"]=="Save":
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
                print("Changes was save",name,note)
            elif request.form["submit_button"]=="Cancel":
                pass
            elif request.form["submit_button"] in fs:
                fs.remove(request.form["submit_button"])
                fsub = ""
                for i,v in enumerate(fs):
                    if i+1==len(fs):
                        fsub+=v
                    else:
                        fsub+=v+"/"
                current_user.favouritesubjects=fsub
                db.session.commit()
                return render_template("editprofile.html",user=current_user,note=usernote,favouritesubjects=enumerate(fs))
            return redirect(url_for("views.profile"))
            
        return render_template("editprofile.html",user=current_user,note=usernote,favouritesubjects=enumerate(fs))
    else:
        return redirect(url_for("auth.login"))
@views.route("/aboutus")
def aboutus():
    return render_template("aboutus.html",user=current_user)

@views.route("/subjects")
def subjects():
    if current_user.is_authenticated:
        return render_template("subjects.html",user=current_user)
    else:
        return redirect(url_for("auth.login"))