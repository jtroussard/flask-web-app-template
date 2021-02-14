from flask import render_template, request, Blueprint, redirect, url_for, flash
from flaskblog.models import Post, User
from flaskblog.config import DATE_FORMAT
from flask_login import current_user

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
@main.route("/home/<show>")
def home(show=None):

	page = request.args.get("page", 1, type=int)
	
	if show:
		User.query.get_or_404(show)
		posts = Post.query.order_by(Post.date_posted.desc()).filter_by(user_id=show).paginate(page=page, per_page=5)
		if not posts.has_next:
			flash(f"This user has not made any posts.", "info")
	else:
		posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template("index.html", posts=posts, title="Home", format=DATE_FORMAT, show=show)
 
@main.route("/about")
def about():
    return render_template('about.html', title="About")

@main.route("/workorders")
def workorders():
    return render_template('workorders.html', title="Work Orders")

@main.route("/workorder/<int:workordernumber>")
def workorder(workordernumber=000000):
    return render_template('workorder.html', workordernumber=workordernumber)

@main.route("/test")
def test():
    return render_template('test.html', title="About")

@main.route("/contact")
def contact():
	return render_template("contact.html")

@main.route("/show_my_posts_only")
def show_my_posts_only():
    return redirect(url_for("main.home", show=current_user.id))