from flask import render_template, redirect, url_for, flash
from . import main
from .forms import PostForm, EditProfileForm, CommentForm
from flask_login import login_required, current_user
from ..models import User, Post, Comment
from .. import db

@main.route('/', methods=['GET', 'POST'])
def index():
	form = PostForm()
	if current_user.is_master and form.validate_on_submit():
		post = Post(body=form.body.data,
					author=current_user._get_current_object()) # attention, 'author' is an instance, so way of assignment is different
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('main.index'))
	posts = Post.query.all()
	return render_template('index.html', form=form, posts=posts)


@main.route('/profile', methods=['GET', 'POST'])
def profile():
	'''if function needs no user's logging in, just query the db to get user info'''
	user = User.query.filter_by(email='flasky_learn@163.com').first()	
	return render_template('about_me.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
	form = EditProfileForm()
	# if this function needs user's logging in, there should be current_user to get user's info
	if current_user.is_master and form.validate_on_submit():
		current_user.username = form.username.data
		current_user.location = form.location.data
		current_user.info = form.info.data
		db.session.add(current_user)
		flash('Your info has been updated!')
		return redirect(url_for('main.profile'))
	form.username.data = current_user.username
	form.location.data = current_user.location
	form.info.data = current_user.info
	return render_template('edit_profile.html', form=form)

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
	post = Post.query.filter_by(id=id).first() # later should use get_or_404 in case the id is invalid in url
	comments = post.comments.order_by(Comment.timestamp.asc())
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(body=form.body.data,
						  post=post)
		db.session.add(comment)
		flash('Your comment has been published!')
		return redirect(url_for('main.post', id=post.id))	
	return render_template('post.html',posts=[post],comments=comments, form=form) 

@main.route('/edit-post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
	form = PostForm()
	post = Post.query.filter_by(id=id).first()
	if current_user.is_master and form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		return redirect(url_for('main.post'))
	form.body.data = post.body
	return render_template('edit_post.html',form=form)