from App1 import app
from App1.controller.forms import LoginForm, RegisterForm

from flask import render_template, redirect, url_for
# from flask_login import login_user, LoginManager, login_required, current_user, logout_user

# -------------------------------------------------------------------
# WITH CRUD on DB
# -------------------------------------------------------------------
@app.route('/register')
def register():
  getForm = RegisterForm()
  return render_template("register.html", form = getForm)


# -------------------------------------------------------------------
# NO CRUD on DB
# -------------------------------------------------------------------
@app.route('/login')
def login():
  getForm = LoginForm()
  return render_template("login.html", form = getForm)


@app.route('/logout')
def logout():
    return redirect(url_for('get_all_posts'))