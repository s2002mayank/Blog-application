# models/ table skeleton same thing
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(150), unique=True)
    username=db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150)) # hashed password
    date_created=db.Column(db.DateTime(timezone=True), default=func.now())
    #relationship
    posts=db.relationship('Post', backref='user', passive_deletes=True)
    comments=db.relationship('Comment', backref='user', passive_deletes=True)
    likes=db.relationship('Like', backref='user', passive_deletes=True)

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.Text, nullable=False)
    date_created=db.Column(db.DateTime(timezone=True), default=func.now())
    #foreign key
    #User corresponds to user(lowercase) model/table as stored in SQL
    # Delete all posts published by the <user> once they are deleted from the database.
    author=db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    #relationship
    comments=db.relationship('Comment', backref='post', passive_deletes=True)
    likes=db.relationship('Like', backref='post', passive_deletes=True)

class Comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.String(180), nullable=False)
    date_created=db.Column(db.DateTime(timezone=True), default=func.now())
    author=db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)    

class Like(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date_created=db.Column(db.DateTime(timezone=True), default=func.now())
    post_id=db.Column(db.Integer, db.ForeignKey('post.id',ondelete='CASCADE'), nullable=False)    
    author=db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

"""
p=Post(...)
p.author -> id (int) ..... 
user=User.query.filter_by(id=id).first()       ----> just to get the user object
user.any_attribute
"""

"""
p=Post(...)
user=p.user                                    -----> got the user object directly
"""
 