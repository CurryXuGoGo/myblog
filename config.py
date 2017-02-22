import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

	SQLALCHEMY_COMMIT_ON_TEARDOWN = True

	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'flasky_learn@163.com'
	MAIL_PASSWORD = 'flasky512'
	FLASKY_MAIL_SUBJECT_PREFIX = '[Curry]'
	FLASKY_MAIL_SENDER = 'Curry Xu <flasky_learn@163.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

	@staticmethod
	def init_app(app):
		pass
		
class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
			'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')

config = {
	'development': DevelopmentConfig,
	'default': DevelopmentConfig
}