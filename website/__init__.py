from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()
DB_name = "LyceumDB"

def create_app():
    app= Flask(__name__)
    app.config["SECRET_KEY"]="SecretKey"
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+DB_name
    db.init_app(app)

    from .auth import auth
    from .views import views
    from .subjects import subjects
    app.register_blueprint(subjects,urlprefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")

    create_databases(app)

    from .models import Users
    login_manager=LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(id)

    return app

def create_databases(app):
    if not path.exists("website/"+DB_name):
        db.create_all(app=app)
        print("Created Database!")
