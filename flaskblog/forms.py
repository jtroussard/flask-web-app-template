from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError

from flaskblog.models import User

class RegistrationForm(FlaskForm):

	# Fields
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=32)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

	# Controlls
	submit = SubmitField('Sign Up')

	# Custom field validations to catch db errors before they reach the backend
	# def validate_field(self, field):
	# 	if true:
	# 		raise ValidationError('Validation Message')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError('That username is not available.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()

		if user:
			raise ValidationError('That email has already been registered.')

class LoginForm(FlaskForm):

	# Fields
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')

	# Controlls
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):

	# Fields
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=32)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
	
	# Controlls
	submit = SubmitField('Update')

	# Custom field validations to catch db errors before they reach the backend
	# def validate_field(self, field):
	# 	if true:
	# 		raise ValidationError('Validation Message')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()

			if user:
				raise ValidationError('That username is not available.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()

			if user:
				raise ValidationError('That email has already been registered.')

class PostForm(FlaskForm):
	# Fields
	title = StringField("Title", validators=[DataRequired()])
	content = TextAreaField("Content", validators=[DataRequired()])
		
	# Controlls
	submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	submit = SubmitField("Request Password Reset")

	def validate_email(self, email):
	user = User.query.filter_by(email=email.data).first()

	if not user:
		raise ValidationError('There is no account with that email. PLease register first.')

class ResetPasswordForm(FlaskForm):
	#Fields
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Reset Password")















