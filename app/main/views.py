from crypt import methods
import imp
import profile
from flask import render_template, redirect, url_for, flash, abort, request
from . import main
from .forms import UpdateProfile, CategoryForm, CommentForm
from flask_login import login_required, current_user
from ..models import User, Post, Category, Comment

@main.route('/')
def index():
    
    posts =  Post.query.order_by(Post.posted.desc()).all()

    return render_template('index.html', posts = posts)

@main.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):

    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)

    posts = Post.get_user_posts(user.id).order_by(Post.posted.desc()).all()

    return render_template('profile/profile.html', user = user, posts = posts)