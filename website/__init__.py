from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_security import Security,SQLAlchemyUserDatastore
from flask_login import LoginManager

db=SQLAlchemy()
DB_Name="Users.db"

def create_app():
    app= Flask(__name__)
    app.config["SECRET_KEY"]="SecretKey"
    app.config["SQLALCHEMY_DATABASE_URI"]=f"sqlite:///{DB_Name}"
    db.init_app(app)

    from .auth import auth
    from .views import views
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")

    from .models import User,Note
    create_databases(app)

    login_manager=LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    user_datastore = SQLAlchemyUserDatastore(db,User,Note)
    security = Security(app, user_datastore)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_databases(app):
    if not path.exists("website/"+DB_Name):
        db.create_all(app=app)
        print("Created Database!")
