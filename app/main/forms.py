from flask_wtf import Form
from flask_pagedown.fields import PageDownField
from ..models import Post
from wtforms.validators import Required, Length
from wtforms import SubmitField,  StringField, TextAreaField

class PostForm(Form):
	body = PageDownField("Write your feelings, lad!", validators=[Required()])
	submit = SubmitField('Submit')

class EditProfileForm(Form):
	username = StringField('How to call me:', validators=[Length(0, 64)])
	location = StringField('Where am I:', validators=[Length(0, 64)])
	info = TextAreaField('About me:')
	sublmit = SubmitField('Submit')

class CommentForm(Form):
	body = StringField('write what you think...', validators=[Length(0,64)])
	submit = SubmitField('Submit')
