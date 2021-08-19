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
        return render_template("profile.html",user=current_user,note=note)
    else:
        return redirect(url_for("auth.login"))

@views.route("/editprofile",methods=["GET","POST"])
def editprofile():
    if current_user.is_authenticated:
        usernote=Notes.query.filter_by(id=current_user.id).first()
        if request.method=="POST":
            if request.form["submit_button"]=="save":
                name = request.form.get("name")
                note = request.form.get("note")
                print(name)
                if name:
                    usern = User.query.filter_by(name=name).first()
                    if not usern:
                        current_user.name=name
                        db.session.commit()
                    else:
                        return redirect(url_for("views.editprofile"))
                usernote.data=note
                db.session.commit()
                print("save",note)
            elif request.form["submit_button"]=="cancel":
                pass
            return redirect(url_for("views.profile"))
        return render_template("editprofile.html",user=current_user,note=usernote)
    else:
        return redirect(url_for("auth.login"))
@views.route("/aboutus")
def aboutus():
    return render_template("aboutus.html",user=current_user)