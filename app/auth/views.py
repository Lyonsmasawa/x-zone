from email import message

from app.email import mail_message
from .. import db
from . import auth
from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User
from ..email import mail_message

@auth.route('/register')
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome To X-ZONE", "email/welcome_user", user.email, user=user)

        return redirect(url_for('auth.login'))

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