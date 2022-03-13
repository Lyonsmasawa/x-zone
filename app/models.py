from curses.ascii import US
from enum import unique
from operator import ge, index
from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,  check_password_hash

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique=True, index = True)
    bio = db.Column(db.String(255))
    pic_path = db.Column(db.String(255), index = True)
    pass_secure = db.Column(db.String(255))

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






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))