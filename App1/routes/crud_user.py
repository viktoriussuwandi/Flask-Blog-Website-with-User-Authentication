from App1 import app, db, add_Post_to_db, hash_salt_passw, check_password, user_only, admin_only
from App1.controller.forms  import User_Login_Form, User_Add_Form, User_Edit_Form_As_Admin, User_Edit_Form_As_User
from App1.controller.models import User, Password

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user

# -------------------------------------------------------------------
def identify_role(mail)      : 
  return "admin" if mail.split("@")[1] == "admin.com" else "user"

def identify_edit_form(find_user) :
  user_edit_form =  User_Edit_Form_As_User(  username = find_user.username, email = find_user.email, 
                                             password = find_user.password.ori_password )
  admin_edit_form = User_Edit_Form_As_Admin( username = find_user.username, email = find_user.email, 
                                             password = find_user.password.ori_password,
                                             role = find_user.role, status   = find_user.status)
  check_user = current_user.role == "user" and current_user.id == user_id
  
# -------------------------------------------------------------------

@app.route('/login', methods = ["GET", "POST"])
def login() :
  if current_user.is_authenticated : return redirect(url_for('get_all_posts'))
  login_form = User_Login_Form()
  form_valid = login_form.validate_on_submit()
  if request.method == "POST" and form_valid :
    mail       = login_form.email.data; passw = login_form.password.data
    find_user  = User.query.filter_by(email=mail).first()
    if not find_user : flash("error : Email is not exist"); return redirect(url_for('add_user'))
    elif find_user.status == "inactive" : flash("error : User is inactive"); return redirect(url_for('login'))
    elif check_password(
      db_passw    = find_user.password.encrypt_password, input_passw = passw 
    ) : login_user(find_user); return redirect(url_for('get_all_posts'))
    else : flash("error : Incorrect email or password"); return redirect(url_for('login'))
  return render_template("login.html", form = login_form, user = current_user)

# -------------------------------------------------------------------

@app.route('/register', methods = ["GET", "POST"] )
def add_user() :
  if current_user.is_authenticated : return redirect(url_for('get_all_posts'))
    
  add_form = User_Add_Form()
  form_valid  = add_form.validate_on_submit()
  
  if request.method == "POST" and form_valid :
    count_user = db.session.query(User).count()
    mail = add_form.email.data; name = add_form.username.data; passw = add_form.password.data
    find_user  = User.query.filter_by(email=mail).first()
    
    if find_user : 
      find_user.status = "active"; db.session.commit()
      flash("error : Email already exist"); return redirect(url_for('login'))
    else :
      new_passw = Password( id = count_user + 1, ori_password = passw, encrypt_password = hash_salt_passw(passw))
      new_user  = User( id = count_user + 1, email = mail, username = name, password = new_passw, role=identify_role(mail) )
      check_add_new_db = add_Post_to_db(new_passw) is not False and add_Post_to_db(new_user) is not False
      if check_add_new_db == True :  flash("error : Register successful"); login_user(new_user); return redirect(url_for('get_all_posts'))
      else : flash("error : Register unsuccessful"); return redirect(url_for('add_user'))
  return render_template("register.html", form = add_form, user = current_user)

# -------------------------------------------------------------------

@app.route('/account_setting/<int:user_id>', methods = ["GET", "POST"] )
@user_only
@admin_only
def edit_user(user_id) :
  find_user  = User.query.get( int(user_id) );  
  edit_form = identify_edit_form(find_user)
  if request.method == "GET" and check_user :
    
  elif request.method == "GET" and current_user.role == "admin" :

  
  elif request.method == "POST" and edit_form.validate_on_submit() :
    pass
  return render_template("register.html", form = edit_form, user = current_user)
  
# -------------------------------------------------------------------

@app.route('/account_close/<int:user_id>', methods = ["GET", "POST"] )
@admin_only
def delete_user(user_id) :
  find_user = User.query.get( int(user_id) );
  find_user.status = "inactive"; db.session.commit()
  if current_user.id == int(user_id) : logout_user(); return redirect(url_for('login'))
  return redirect(url_for('get_all_posts'))

# -------------------------------------------------------------------

@app.route('/logout')
def logout():
  if current_user.is_authenticated: logout_user()
  return redirect(url_for('get_all_posts'))