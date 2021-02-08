import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)

	output_size = (250, 250)
	new_size_img = Image.open(form_picture)
	new_size_img.thumbnail(output_size)
	new_size_img.save(picture_path)

	return (picture_fn)

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message("Password Reset Request", 
		sender="tekksparrow.mail_service@yahoo.com", 
		recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:\n
{url_for("users.reset_token", token=token, _external=True)}\n\n
If you did not make this request then simply ignore this email. No chnages will be made to your account.
'''
	mail.send(msg)	