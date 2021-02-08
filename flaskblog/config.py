import os


# Default Settings - Can set some constants or default variables here. e.g. No database URI is returned we can use a sqlite db.

# Application Constants
# Application Constants
DATE_FORMAT = "%A, %B %d, %Y"

class Config:
	# Application configurations
	SECRET_KEY                 = os.environ.get("SECRET_KEY")

	# Database configurations
	SQLALCHEMY_DATABASE_URI    = os.environ.get("SQLALCHEMY_DATABASE_URI")

	# Email server stuff
	MAIL_SERVER                = "smtp.mail.yahoo.com"
	MAIL_PORT                  = 587
	MAIL_USE_TLS               = True
	MAIL_USE_SSL               = False
	# MAIL_DEBUG               = True

	MAIL_USERNAME              = os.environ.get("EMAIL_USER")
	MAIL_PASSWORD              = os.environ.get("EMAIL_PASS")