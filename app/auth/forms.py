from ast import In, Str
from operator import imod
from flask_wtf import FlaskForm
from importlib_metadata import email
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Enter Your Email: ', validators=[InputRequired(), Email()])
    username = StringField('Enter Username: ', validators=[InputRequired()])
    password = PasswordField('Enter Password: ',validators=[InputRequired(),EqualTo('password_confirm', message='Passwords must match!')])
    password_confirm = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Enter Your Email: ', validators=[InputRequired(), Email()])
    password = PasswordField('Enter Password: ',validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')
    