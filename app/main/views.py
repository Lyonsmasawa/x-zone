from operator import pos
from flask import render_template, redirect, url_for, flash, abort, request
from . import main
from .forms import UpdateProfile, CommentForm
from flask_login import login_required, current_user
from ..models import User, Post, Category, Comment
from app import db, photos
from ..requests import random_quotes

@main.route('/')
def index():
    
    posts =  Post.query.order_by(Post.posted.desc()).all()

    quote = random_quotes()

    return render_template('index.html', posts = posts, quotes = quote)

@main.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):

    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)

    posts = Post.get_user_posts(user.id).order_by(Post.posted.desc()).all()

    
    comments = Comment.get_comments()

    return render_template('profile/profile.html', user = user, posts = posts, comments=comments)

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
    
    return render_template('profile/update_profile.html', form=form)

@main.route('/profile/<username>/update/pic', methods = ['POST'])
def update_pic(username):

    user = User.query.filter_by(username=username).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.pic_path = path
        db.session.commit()
    
    return redirect(url_for('main.profile', username=username))

@main.route('/add_post', methods = ['GET', 'POST'])
def add_post():
    title = request.args.get('title')
    content = request.args.get('content')
    user_id = request.args.get('user_id')

    add_post = Post(title = title, body = content, user_id=user_id )
    db.session.add(add_post)
    db.session.commit()

    flash('Post created successfully', 'success')

    return redirect(url_for('main.profile', username = current_user.username))

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    comments = Comment.query.filter_by(post_id = id).all()
    post = Post.query.get(id)
    if post is None:
        abort(404)

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment = form.comment.data, post_id = id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        
        return redirect(url_for('.post', id=post.id ))

    return render_template('post.html', post=post, form=form, comments = comments)


@main.route('/post/<int:id>/edit_post', methods = ['GET', 'POST'])
def edit_post(id):

    post = Post.get_single_post(id)

    title = request.args.get('title')
    content = request.args.get('content')

    post.title = title
    post.body = content
    post.title = title

    db.session.commit()

    flash('Changes saved', 'success')

    return redirect(url_for('main.profile', username = current_user.username))

@main.route('/post/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.get_single_post(id)
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted')

    return redirect(url_for('main.profile', username=current_user.username))

@main.route('/post/<int:id>/delete_comment', methods=['GET', 'POST'])
def delete_comment(id):
    comment = Comment.get_comments(id)
    db.session.delete(comment)
    db.session.commit()

    flash('Comment deleted')

    return redirect(url_for('main.profile', username=current_user.username))