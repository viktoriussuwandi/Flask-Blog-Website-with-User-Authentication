from App1 import app, db, add_Post_to_db, hash_salt_passw, check_password, user_only, admin_only
from App1.controller.forms  import LoginForm, RegisterForm
from App1.controller.models import User, Password

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user

# -------------------------------------------------------------------
def identify_role(mail) : return "admin" if mail.split("@")[1] == "admin.com" else "user"

# -------------------------------------------------------------------

@app.route('/register', methods = ["GET", "POST"] )
def add_user() :
  regist_form = RegisterForm()
  form_valid  = regist_form.validate_on_submit()
  # while do not registered
  if request.method == "POST" and form_valid :
    count_user = db.session.query(User).count()
    mail = regist_form.email.data; name = regist_form.username.data; passw = regist_form.password.data
    find_user  = User.query.filter_by(email=mail).first()
    if find_user : flash("error : Email already exist"); return redirect(url_for('add_user'))
    else :
      new_passw = Password( id = count_user + 1, ori_password = passw, encrypt_password = hash_salt_passw(passw))
      new_user  = User( id = count_user + 1, email = mail, username = name, password = new_passw, role=identify_role(mail) )
      check_add_new_db = add_Post_to_db(new_passw) is not False and add_Post_to_db(new_user) is not False
      if check_add_new_db == True : login_user(new_user); return redirect(url_for('get_all_posts'))
      else : flash("error : Register unsuccessful"); return redirect(url_for('add_user'))
  return render_template("register.html", form = regist_form, user = current_user)

# -------------------------------------------------------------------

@app.route('/account_config/<int:user_id>', methods = ["GET", "POST"] )
@user_only
@admin_only
def edit_user(user_id) :
  pass

# -------------------------------------------------------------------

@app.route('/account_close/<int:user_id>', methods = ["GET", "POST"] )
@admin_only
def delete_user(user_id) :
  find_user = User.query.get( int(user_id) ); db.session.delete(find_user); db.session.commit()
  return redirect(url_for('get_all_posts'))
  
# -------------------------------------------------------------------
@app.route('/login', methods = ["GET", "POST"])
def login() :
  login_form = LoginForm()
  form_valid = login_form.validate_on_submit()
  if request.method == "POST" and form_valid :
    mail       = login_form.email.data; passw = login_form.password.data
    find_user  = User.query.filter_by(email=mail).first()
    if not find_user : flash("error : Email is not exist"); return redirect(url_for('add_user'))
    elif check_password(
      db_passw = find_user.password.encrypt_password, 
      input_passw = passw 
    ) : login_user(find_user); return redirect(url_for('get_all_posts'))
    else : flash("error : Incorrect email or password"); return redirect(url_for('login'))
  return render_template("login.html", form = login_form, user = current_user)

# -------------------------------------------------------------------
@app.route('/logout')
def logout():
  if current_user.is_authenticated: logout_user()
  return redirect(url_for('get_all_posts'))