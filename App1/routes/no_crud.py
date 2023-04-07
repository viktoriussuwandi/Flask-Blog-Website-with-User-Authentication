from App1 import app
from App1.controller.models import BlogPost, User, Comment
from flask import render_template
from flask_login import current_user

@app.route('/')
def get_all_posts():
  posts    = BlogPost.query.all()
  users    = User.query.all()
  comments = Comment.query.all()
  return render_template("index.html", 
                         all_posts=posts, 
                         all_users=users, 
                         all_comments=comments,
                         user = current_user
                        )

@app.route("/about")
def about():
    return render_template("about.html", user = current_user)

@app.route("/contact")
def contact():
    return render_template("contact.html", user = current_user)