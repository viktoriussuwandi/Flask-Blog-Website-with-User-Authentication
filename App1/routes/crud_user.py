from App1 import app, db, add_Post_to_db, hash_salt_passw, check_password
from App1.controller.forms import LoginForm, RegisterForm
from App1.controller.models import User, Password
from flask import render_template, redirect, url_for, request, flash
# from flask_login import login_user, LoginManager, login_required, current_user, logout_user

# -------------------------------------------------------------------
# WITH CRUD on DB
# -------------------------------------------------------------------
@app.route('/register', methods = ["GET", "POST"] )
def register():
  regist_form = RegisterForm()
  form_valid  = regist_form.validate_on_submit()
  count_user  = db.session.query(User).count()
  # while do not registered
  if request.method == "POST" and form_valid :
    mail      = regist_form.email.data
    find_user = User.query.filter_by(email=mail).first()
    if find_user : flash("error : Email already exist");
    else :
      new_passw = Password( id = count_user + 1, 
        ori_password     = regist_form.passw.data,
        encrypt_password = hash_salt_passw(regist_form.passw.data)
      )
      new_user = User( id = count_user + 1, email = mail,
        username = regist_form.username.data, password = new_passw
      )
      if add_Post_to_db(new_passw) is not False and add_Post_to_db(new_user) is not False :
        return redirect(url_for('get_all_posts'))
        
  return render_template("register.html", form = regist_form)


# -------------------------------------------------------------------
# NO CRUD on DB
# -------------------------------------------------------------------
@app.route('/login', methods = ["GET", "POST"])
def login():
  login_form = LoginForm()
  
  return render_template("login.html", form = login_form)


@app.route('/logout')
def logout():
    return redirect(url_for('get_all_posts'))