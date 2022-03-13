from .. import db
from . import auth
from flask import render_template
from flask_login import login_user, logout_user, login_required
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User

@auth.route('/register')
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()

    

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