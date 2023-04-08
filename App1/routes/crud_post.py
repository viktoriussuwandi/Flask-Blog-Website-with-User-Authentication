from App1 import app, db, add_data_to_db
from App1.controller.forms  import Post_Add_Form
from App1.controller.models import User, BlogPost

from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, login_required, current_user, logout_user
from datetime import date

@app.route("/post/<int:post_id>")
def show_post(post_id):
  requested_post = BlogPost.query.get(post_id)
  return render_template("post.html", post = requested_post)

@app.route("/create_post")
def add_post():
    add_form = Post_Add_Form()
    if add_form.validate_on_submit() :
        new_post     = BlogPost(
            title    = add_form.title.data,
            subtitle = add_form.subtitle.data,
            body     = add_form.body.data,
            img_url  = add_form.img_url.data,
            author   = current_user,
            date     = date.today().strftime("%B %d, %Y")
        )
        if add_data_to_db(new_post) == True : flash("Article successfully posted", "success"); return redirect(url_for('get_all_posts'))
        else : flash(" Posted unsuccessful", "danger"); return redirect(url_for('add_post'))
    return render_template("create_post.html", form = add_form )

@app.route("/update_post/<int:post_id>")
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = Post_Add_Form(
        title    = post.title,
        subtitle = post.subtitle,
        img_url  = post.img_url,
        author   = post.author,
        body     = post.body
    )
    if edit_form.validate_on_submit():
        post.title    = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url  = edit_form.img_url.data
        post.author   = edit_form.author.data
        post.body     = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)

@app.route("/delete_post/<int:post_id>")
def close_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))
