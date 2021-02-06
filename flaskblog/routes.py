import secrets, os
from PIL import Image
from flaskblog import app, db, bcrypt, mail
from flask import render_template, send_from_directory, url_for, flash, redirect, request, abort
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

DATE_FORMAT = "%A, %B %d, %Y"

@app.route("/")
@app.route("/home")
@app.route("/home/<show>")
def home(show=None):

	page = request.args.get("page", 1, type=int)

	if show:
		posts = Post.query.order_by(Post.date_posted.desc()).filter_by(user_id=show).paginate(page=page, per_page=5)
	else:
		posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template("index.html", posts=posts, title="Home", format=DATE_FORMAT, show=show)
 
@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/workorders")
def workorders():
    return render_template('workorders.html', title="Work Orders")

@app.route("/workorder/<int:workordernumber>")
def workorder(workordernumber=000000):
    return render_template('workorder.html', workordernumber=workordernumber)

@app.route("/test")
def test():
    return render_template('test.html', title="About")

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/reg", methods=['GET', 'POST'])
def reg():

	if (current_user.is_authenticated):
		return redirect(url_for("home"))

	form = RegistrationForm()

	if form.validate_on_submit() and request.method == "POST":
		try:
			hashed_pass = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
			user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
			db.session.add(user)
			db.session.commit()
			flash(f"Your account has now been created for {form.username.data}. Please login.", "success")
			return redirect(url_for('login'))
		except:
			# TODO add logging
			flash("Database error. Contact Administrator", "danger")
	return render_template('reg.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if (current_user.is_authenticated):
		return redirect(url_for("home"))

	if form.validate_on_submit() and request.method == "POST":
		user = User.query.filter_by(email=form.email.data).first()

		if user and bcrypt.check_password_hash(user.password, form.password.data) : #(db-pass, form-pass) 
			login_user(user, remember=form.remember.data)
			next_page = request.args.get("next") # Using method instead of accessing the index directly will prevent errors when the dict value is null/nothing/missing
			flash("You have been logged in!", "success")
			return redirect(url_for(next_page)) if next_page else redirect(url_for("home"))
		else:
			flash("Login in unsuccessful. Check email and password values.", "danger")

	return render_template('login.html', title="Login", form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

	output_size = (250, 250)
	new_size_img = Image.open(form_picture)
	new_size_img.thumbnail(output_size)
	new_size_img.save(picture_path)

	return (picture_fn)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():	
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file

		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Your account information has been updated", "success")
		return redirect(url_for("account")) # POST GET redirect pattern
	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for("static", filename='profile_pics/' + current_user.image_file)
	print(current_user.image_file)
	return render_template("account.html", title="Account", image_file=image_file, form=form)

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
	form = PostForm()

	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)

		db.session.add(post)
		db.session.commit()
		flash(f"Your post has been created.", "success")
		return redirect(url_for("home"))
	return render_template("create_post.html", title="New Post", form=form, legend="New Post")	

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template("post.html", title=post.title, post=post, format=DATE_FORMAT)	

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)

	if post.author != current_user:
		abort(403)

	form = PostForm()

	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash("Your post has been updated", "success")
		return redirect(url_for("post", post_id=post_id))
	elif request.method == "GET":
		form.title.data = post.title
		form.content.data = post.content

	return render_template("create_post.html", title="New Post", form=form, format=DATE_FORMAT, legend="Update Post")	

@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)

	if post.author != current_user:
		abort(403)

	db.session.delete(post)
	db.session.commit()
	flash(f"Your post has been deleted", "success")
	return redirect(url_for("home"))

@app.route("/show_my_posts_only")
def show_my_posts_only():
    return redirect(url_for("home", show=current_user.id))

@app.route("/show_all_posts")
def show_all_posts():
    return redirect(url_for("home", show=None))

@app.route("/")
@app.route("/user/<string:username>")
def user_posts(username):
	page = request.args.get("page", 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template("user_post.html", posts=posts, user=user, format=DATE_FORMAT)

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message("Password Reset Request", 
		sender="tekksparrow.help@gmail.com", 
		recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:\n
{url_for("reset_token", token=token, _external=True)}\n\n
If you did not make this request then simply ignore this email. No chnages will be made to your account.
'''

@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():

	if (current_user.is_authenticated):
		return redirect(url_for("home"))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash("An email has been sent with instructions to reset your password.", "info")
		return redirect(url_for("login"))
	return render_template("reset_request.html", title="Reset Password", form=form)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):

	if (current_user.is_authenticated):
		return redirect(url_for("home"))
	
	user = User.verify_reset_token(token)
	if user is None:
		flash("That is an invalid or expired token", "warning")
		return redirect(url_for("reset_request"))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user.password = hashed_pass
		db.session.commit()
		flash(f"Your password has been updated. Please login.", "success")
		return redirect(url_for('login'))
	return render_template("reset_token.html", title="Reset Password", form=form)