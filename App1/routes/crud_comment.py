from App1                   import app, db, add_data_to_db, admin_only
from App1.controller.forms  import Comment_Add_Form
from App1.controller.models import BlogPost, Comment

from flask       import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user

# -------------------------------------------------------------------
# ADDITIONAL FUNTION
# -------------------------------------------------------------------

def is_authorized(post) :
  return (
    current_user.is_authenticated and current_user.role == "admin" and current_user.status == "active"
    or ( post.status == "active" and
         current_user.is_authenticated   and current_user.id    == post.author.id and
         current_user.status == "active" and current_user.email == post.author.email
       )
  )

# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------

@app.route("/post/<int:post_id>", methods = ["GET", "POST"])
def show_post(post_id) :
  find_post     = BlogPost.query.get(post_id)
  post_comments = Comment.query.filter_by(post_id=find_post.id).all()
  count_comment = Comment.query.count()
  add_form      = Comment_Add_Form(); form_valid = add_form.validate_on_submit()
  if request.method == "POST" and form_valid :
    new_comment   = Comment(
      id     = count_comment + 1,
      text   = add_form.text.data,
      posts  = find_post,
      author = find_post.author
    )
    if not is_authorized(find_post) : abort(401)
    elif   add_data_to_db(new_comment) is not False : flash("comment posted", "success")
    else : flash("comment failed", "danger")
  return render_template("post.html", 
                         user = current_user, post = find_post,
                         comments = post_comments,form = add_form, 
                         is_authorized_user = is_authorized(find_post))


@app.route("/activation_comment/<int:comment_id>")
@admin_only
def config_comment(comment_id) :
  find_comment = Comment.query.get(comment_id)
  find_comment.status = "active" if find_comment.status == "inactive" else "inactive"
  db.session.commit()
  
  # Return to post
  find_post    = BlogPost.query.get(find_comment.post_id)
  post_comments = Comment.query.filter_by(post_id=find_post.id).all()
  add_form     = Comment_Add_Form()
  return  redirect( url_for("show_post",
                            post_id = find_post.id,
                            user = current_user, post = find_post,
                            comments = post_comments,form = add_form, 
                            is_authorized_user = is_authorized(find_post)
                           ))
  
  