from curses.ascii import US
from enum import unique
from operator import ge, index
from unicodedata import category
from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,  check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique=True, index = True)
    bio = db.Column(db.String(255))
    pic_path = db.Column(db.String(255), index = True)
    pass_secure = db.Column(db.String(255))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You are not allowed to do this')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    @staticmethod
    def verify_email(email):
        return User.query.filter_by(email = email).first()

    def __repr__(self):
        return f'User {self.username}'

class Category(db.Model):
    
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(255))
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'User {self.category}'

class Post(db.Model):

    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255))
    peek = db.Column(db.String(255))
    posted = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'User {self.title}'




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))