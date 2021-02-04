import logging, traceback
from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin


# This will manage sessions
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# You can make your own table names via attrs
class User(db.Model, UserMixin):

	#columns
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(50), nullable=False, default="default.jpeg")
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship("Post", backref="author", lazy=True) 

	def __repr__(self):
		return f"User: {self.username}, {self.email}, {self.image_file}"

class Post(db.Model):

	#columns
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	status = db.Column(db.Integer, default=0)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

	def get_formatted_date(self, format):
		formatted_string = str(self.date_posted.strftime(format))
		return formatted_string

	def __repr__(self):
		return f"Post: {self.title}, {self.date_posted}"