from curses.ascii import US
from email.policy import default
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
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You are not allowed to do this')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

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
    posted = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_single_post(cls, id):
        post = Post.query.filter_by(id=id).first()
        return post

    @classmethod
    def get_all_posts(cls):
        posts = Post.query.all()
        return posts

    @classmethod
    def get_user_posts(cls, user_id):
        posts = Post.query.filter_by(user_id=user_id)
        return posts
    
    @classmethod
    def get_posts_by_category(cls, category_id):
        posts = Post.query.filter_by(category_id=category_id)
        return posts

    @classmethod
    def get_posts_comments(self):
        comments = Comment.query.filter_by(post_id = self.id)
        return comments

    def __repr__(self):
        return f'User {self.title}'


class Comment(db.Model):

    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(255))
    posted_at = db.Column(db.DateTime, default = datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_comments(cls):
        comments = Comment.query.all()
        return comments
    
    @classmethod
    def get_single_comment(cls, id):
        comment = Comment.query.filter_by(id=id).first()
        return comment

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))