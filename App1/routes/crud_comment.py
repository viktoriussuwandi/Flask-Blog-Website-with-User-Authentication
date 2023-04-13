from App1                   import app, add_data_to_db, user_only
from App1.controller.forms  import Comment_Add_Form
from App1.controller.models import BlogPost, Comment

from flask       import render_template, flash, request, abort
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
def show_post(post_id):
  find_post     = BlogPost.query.get(post_id)
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
  return render_template("post.html", post = find_post, user = current_user, 
                         form = add_form, is_authorized_user = is_authorized(find_post))