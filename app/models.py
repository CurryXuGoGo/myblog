from flask_login import UserMixin
from . import db, login_manager # import instance from __init__.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin): # two father-class??
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128)) # don't save the password itself
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	location = db.Column(db.String(64))
	info = db.Column(db.Text())
	
	@property
	def password(self):
		raise AttributeError('Password is not a readable attribute.')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	@property
	def is_master(self):
		return self.email == 'flasky_learn@163.com'

@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))

class Post(db.Model):
	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	comments= db.relationship('Comment', backref='post', lazy='dynamic')

class Comment(db.Model):
	__tablename__ = 'comments'

	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

