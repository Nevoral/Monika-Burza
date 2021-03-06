from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .flash_toastr import Toastr
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app =  Flask(__name__)
    toastr = Toastr(app)
    app.config['SECRET_KEY'] = 'idontcare'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix="/")
    
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Burza
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("web/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")