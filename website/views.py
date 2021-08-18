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

@views.route("/user")
def user():
    if current_user.is_authenticated:
        return render_template("user.html",user=current_user)
    else:
        return redirect(url_for("auth.login"))

class EditUser(FlaskForm):
    email = StringField("Email", [validators.Length(5,64, message="velikost majliku musí být od 5 do 64 znaků"),validators.Email(message="Zadáváš mi špatný email")])
    name = StringField("Name", [validators.Length(5,20,message="velikost jména musí být od 5 do 20 znaků")])
    submit = SubmitField("Save")

@views.route("/edituser",methods=["GET","POST"])
def edituser():
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

            return redirect(url_for("views.user"))
        return render_template("edituser.html",user=current_user,form=form)
    else:
        return redirect(url_for("auth.login"))