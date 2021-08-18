from flask import render_template, Blueprint,request,redirect, url_for,flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,validators,Form
from wtforms.validators import InputRequired,Length,Email,EqualTo
from validate_email import validate_email


auth=Blueprint("auth", __name__)


class RegisterForm(FlaskForm):
    email = StringField("Email", [validators.InputRequired(message="Email potřebuji"), validators.Length(5,64, message="velikost majliku musí být od 5 do 64 znaků"),validators.Email(message="Zadáváš mi špatný email")])
    name = StringField("Name", [validators.InputRequired(message="Email potřebuji"), validators.Length(5,20,message="velikost jména musí být od 5 do 20 znaků")])
    password1 = PasswordField("Password1", [validators.InputRequired(message="Heslo potřebuji"), validators.Length(5,24),validators.EqualTo("password2",message="Password must match")])
    password2 = PasswordField("Password2")
    submit = SubmitField("Log In")


@auth.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("views.user"))
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        usere = User.query.filter_by(email=form.email.data).first()
        usern = User.query.filter_by(name=form.name.data).first()
        if not usere:
            if not usern:
                new_user = User(email=form.email.data,name=form.name.data,password=generate_password_hash(form.password1.data, method="sha256"))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash("Account created!", category="success")
                print("Account was created succesfully, welcome",form.name.data)
                return redirect(url_for("views.home"))
            else:
                flash("Please use different name.",category="error")
        else:
            flash("Please use different email account.",category="error")
    return render_template("register.html",user=current_user,form=form)

class LoginForm(FlaskForm):
    email = StringField("Email", [validators.InputRequired(), validators.Length(5,64),validators.Email()])
    password = PasswordField("Password", [validators.InputRequired(), validators.Length(5,24)])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log In")

@auth.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.user"))
    form = LoginForm(request.form)
    print(form.errors)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect (url_for("views.home"))
            else:
                flash("Incorrect password, try again.",category="error")
        else:
            flash("Email does not exist.",category="error")
    return render_template("login.html", user=current_user,form=form)


@auth.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("auth.login"))

