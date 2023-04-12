from App1 import app, db, add_data_to_db, user_only, admin_only
from App1.controller.forms  import Post_Add_Form
from App1.controller.models import User, BlogPost

from flask       import render_template, redirect, url_for, request, flash, abort
from flask_login import current_user
from datetime import date

# -------------------------------------------------------------------
# ADDITIONAL FUNTION
# -------------------------------------------------------------------
def is_authorized(post) :
  author    = User.query.get(post.author_id)
  checkings = (current_user.role == "admin" and current_user.email.split("@")[1] == "admin.com") or (
    current_user.id == author.id and current_user.role == author.role)
  return checkings

# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------
@app.route("/post/<int:post_id>")
def show_post(post_id):
  requested_post = BlogPost.query.get(post_id)
  return render_template("post.html", post = requested_post)

@app.route("/create_post", methods = ["GET", "POST"])
@user_only
def add_post() :
  add_form   = Post_Add_Form(); form_valid = add_form.validate_on_submit()
  if request.method == "POST" and form_valid :
    count_post = db.session.query(BlogPost).count()
    new_post   = BlogPost(
      id       = count_post + 1,
      title    = add_form.title.data,
      subtitle = add_form.subtitle.data,
      body     = add_form.body.data,
      img_url  = add_form.img_url.data,
      author   = current_user,
      date     = date.today().strftime("%B %d, %Y")
    )
    if add_data_to_db(new_post) is not False : 
      flash("Article successfully posted", "success"); return redirect( url_for('get_all_posts') )
    else : 
      flash(" Posted unsuccessful", "danger"); return redirect( url_for('add_post') )
  return render_template("make-post.html", form = add_form, user = current_user, is_edit = False )

@app.route("/update_post/<int:post_id>")
def edit_post(post_id) :
  post = BlogPost.query.get(post_id)
  if not is_authorized(post) : return abort(401)
  else :
    edit_form  = Post_Add_Form(
      title    = post.title,
      subtitle = post.subtitle,
      img_url  = post.img_url,
      author   = post.author,
      body     = post.body
    )
    if edit_form.validate_on_submit() :
      post.title    = edit_form.title.data
      post.subtitle = edit_form.subtitle.data
      post.img_url  = edit_form.img_url.data
      post.author   = edit_form.author.data
      post.body     = edit_form.body.data
      db.session.commit()
      return redirect( url_for("show_post", post_id=post.id) )
  return render_template("make-post.html", form=edit_form, user = current_user)

@app.route("/close_post/<int:post_id>")
def delete_post(post_id) :
  find_post = BlogPost.query.get( int(post_id) );
  if find_post : find_post.status = "inactive"; db.session.commit()
  return redirect(url_for('get_all_posts'))
