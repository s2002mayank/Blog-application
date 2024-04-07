#website\__init__.py
from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy() #database object?
DB_NAME= "database.db"

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']="PROCRASTINATION"
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    # blueprint => views
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment, Like
    create_database(app) 

    login_manager=LoginManager()
    login_manager.login_view= 'auth.login'
    login_manager.init_app(app)

    '''
    This sets the callback for reloading a user from the session.
    The function you set should take a user ID (a str) and return a user object,
    or None if the user does not exist.
    '''

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()  
