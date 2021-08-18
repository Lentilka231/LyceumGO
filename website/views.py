from flask import Blueprint, render_template, redirect, url_for,request,flash
from flask_login import login_required,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,validators,Form
from .models import User
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
        return render_template("profile.html",user=current_user)
    else:
        return redirect(url_for("auth.login"))

class EditUser(FlaskForm):
    name = StringField("Name", [validators.Length(5,20,message="velikost jména musí být od 5 do 20 znaků")])
    submit = SubmitField("Save")

@views.route("/editprofile",methods=["GET","POST"])
def editprofile():
    if current_user.is_authenticated:
        form=EditUser(request.form)
        if form.validate_on_submit():
            usere = User.query.filter_by(email=form.email.data).first()
            usern = User.query.filter_by(name=form.name.data).first()
            print("tady")
            if not usere:
                if not usern:
                    print(form.name.data)
                    if form.name.data:
                        current_user.name=form.name.data
                        db.session.commit()

            return redirect(url_for("views.profile"))
        return render_template("editprofile.html",user=current_user,form=form)
    else:
        return redirect(url_for("auth.login"))