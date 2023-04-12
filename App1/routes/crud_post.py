from App1 import app, db, add_data_to_db, user_only, admin_only
from App1.controller.forms  import Post_Add_Form, Post_Edit_Form_As_Admin, Post_Edit_Form_As_User
from App1.controller.models import BlogPost

from flask       import render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from datetime import date

# -------------------------------------------------------------------
# ADDITIONAL FUNTION
# -------------------------------------------------------------------
def is_authorized(post) :
  return (
    current_user.is_authenticated and current_user.role == "admin" and current_user.status == "active"
  ) or (
    current_user.is_authenticated   and current_user.id == post.author.id and
    current_user.status == "active" and current_user.email == post.author.email
  )

def identify_edit_form(find_post) :
  is_authorize_admin = is_authorized(find_post) and current_user.role == "admin"
  is_authorize_user  = is_authorized(find_post) and current_user.role == "user"
  if is_authorize_admin :
    return Post_Edit_Form_As_Admin(
      status   = find_post.status,  title  = find_post.title,  subtitle = find_post.subtitle,
      img_url  = find_post.img_url, author = find_post.author.username, body    = find_post.body
    )    
  elif is_authorize_user :
    return Post_Edit_Form_As_User(
      title   = find_post.title,  subtitle = find_post.subtitle,
      img_url = find_post.img_url, author  = find_post.author.username, body    = find_post.body
    )
  else : return abort(401)

def update_postInfo(find_post, form) :
  check_admin = is_authorized(find_post) and current_user.role == "admin"
  if check_admin : find_post.status   = form.status.data
  find_post.title    = form.title.data
  find_post.subtitle = form.subtitle.data
  find_post.img_url  = form.img_url.data
  find_post.author   = form.author.data
  find_post.body     = form.body.data
  
  if is_authorized(find_post) :
    try : db.session.commit(); return True
    except Exception : db.session.rollback(); return False
  else : return False
    
# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------
@app.route("/post/<int:post_id>")
def show_post(post_id):
  requested_post = BlogPost.query.get(post_id)
  return render_template("post.html", post = requested_post, 
                         user = current_user, is_authorized_user = is_authorized(requested_post))

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
  return render_template("make-post.html", form = add_form, user = current_user, activity = "posting" )

@app.route("/update_post/<int:post_id>", methods = ["GET", "POST"])
@login_required
def edit_post(post_id) :
  find_post  = BlogPost.query.get(post_id)
  if not is_authorized(find_post) : return abort(401)
  else :
    edit_form  = identify_edit_form(find_post); form_valid = edit_form.validate_on_submit()
    if request.method == "POST" and form_valid :
      if not update_postInfo(find_post, edit_form) :
        flash("update post unsuccessful", "danger")
        return redirect(url_for("make-post.html", form = edit_form, user = current_user, activity = "editing" ))
      elif update_postInfo(find_post, edit_form) :
        flash("update profile successful", "success")
        return redirect( url_for("show_post", post_id = find_post.id) )
  return render_template("make-post.html", form = edit_form, user = current_user, activity = "editing" )

@app.route("/close_post/<int:post_id>")
@admin_only
def delete_post(post_id) :
  find_post = BlogPost.query.get( int(post_id) );
  if find_post : find_post.status = "inactive"; db.session.commit()
  return redirect(url_for('get_all_posts'))
