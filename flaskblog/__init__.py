# Initialize the application and bring together necessary compoenents
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sqlalchemy import orm
from flask_login import LoginManager
from flask_mail import Mail

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.__static_folder = "./static/"


# Application configurations
app.config["SECRET_KEY"] = "RandomCharacters" # Make this an environment variable later
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"


# Database Stuff
db = SQLAlchemy(app) # classes == database models
migrate = Migrate(app, db)


# Login/Hashing
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login" # Make sure this is the function name of the desired route
login_manager.login_message_category = "info"

# Email server stuff
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USER")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")
mail = Mail(app)

# Circular import error if this is created before the app variable
from flaskblog import routes