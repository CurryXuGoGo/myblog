from ..models import User
from .. import db
from . import auth
from .forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user

@auth.route('/')
def index():
	return '<h1>hello!</h1>'

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data) # this 'password' is a class method actually, not a variable
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('auth.login')) # return redirect link
	return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('auth.index'))

