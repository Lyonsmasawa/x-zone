from crypt import methods
from inspect import _void
from .. import db
from . import auth
from flask import render_template
from flask_login import login_user, logout_user, login_required
from app.auth.forms import RegistrationForm, LoginForm

@auth.route('/register')
def register():
    form = RegistrationForm()

    return render_template('auth/register.html', register_form = form)

@auth.route('/login')
def login():
    login_form = LoginForm()
    return render_template('auth/login.html', login_form = login_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return