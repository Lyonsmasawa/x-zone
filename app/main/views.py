from flask import render_template, redirect, url_for, flash, abort, request
from . import main
from .forms import UpdateProfile, CategoryForm, CommentForm
from flask_login import login_required, current_user
from ..models import User, Post, Category, Comment
from app import db, photos

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

@main.route('/profile/<username>/update', methods = ['GET', 'POST'])
def update_profile(username):

    user = User.query.filter_by(username=username).first()

    if user is None:
        abort(404)
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', username=user.username))
    
    return render_template('profile/update_profile.html')

@main.route('/profile/<username>/update/pic', methods = ['POST'])
def update_pic(username):

    user = User.query.filter_by(username=username).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.pic_path = path
        db.session.commit()
    
    return redirect(url_for('main.profile', username=username))