from crypt import methods
from .. import db
from . import auth
from flask import render_template
from app.auth.forms import RegistrationForm, LoginForm

@auth.route('/register', methods = ["GET", "POST"])
def register():
    form = RegistrationForm()

    return render_template('register.html', register_form = form)

@auth.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()

    return render_template('register.html', login_form = form)