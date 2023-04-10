from App1 import app, db, add_data_to_db, hash_salt_passw, check_password, admin_only
from App1.controller.forms  import User_Login_Form, User_Add_Form, User_Edit_Form_As_Admin, User_Edit_Form_As_User
from App1.controller.models import User, Password

from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, login_required, current_user, logout_user

# -------------------------------------------------------------------
# ADDITIONAL
# -------------------------------------------------------------------
def identify_role(mail) : return "admin" if mail.split("@")[1] == "admin.com" else "user"

def identify_edit_form(find_user) :
  is_authorize_admin = (current_user.role == "admin" and current_user.status == "active" and find_user.role == "user") or (
                        current_user.role == "admin" and current_user.status == "active" and current_user.id == find_user.id)
  is_authorize_user  = (current_user.role == "user"  and current_user.status == "active" and current_user.id == find_user.id)
  if is_authorize_admin :
    return User_Edit_Form_As_Admin( username = find_user.username, email = find_user.email,
                                    password = find_user.password.ori_password, role = find_user.role, status = find_user.status)
  elif is_authorize_user :
    return User_Edit_Form_As_User( username = find_user.username, email = find_user.email, 
                                   password = find_user.password.ori_password )
  else : return abort(401)

def update_userInfo(find_user, form) :
  if current_user.role == "admin" : find_user.role = form.role.data; find_user.status = form.status.data
  find_user.username = form.username.data
  find_user.email    = form.email.data
  find_user.password.ori_password = form.password.data
  find_user.password.encrypt_password = hash_salt_passw(form.password.data)
  try : db.session.commit(); return True
  except Exception : db.session.rollback(); return False

# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------
@app.route('/login', methods = ["GET", "POST"])
def sign_in() :
  if current_user.is_authenticated : flash("User already login", "danger"); return redirect(url_for('get_all_posts'))
  login_form = User_Login_Form()
  form_valid = login_form.validate_on_submit()
  if request.method == "POST" and form_valid :
    mail       = login_form.email.data; passw = login_form.password.data
    find_user  = User.query.filter_by(email=mail).first()
    if not find_user : flash("Email is not exist", "danger"); return redirect(url_for('add_user'))
    elif find_user.status == "inactive" : 
      flash("User is inactive", "danger")
      return redirect(url_for('sign_in'))
    elif check_password(db_passw    = find_user.password.encrypt_password, input_passw = passw ) : 
      flash("Login Success", "success"); login_user(find_user)
      return redirect(url_for('get_all_posts'))
    else : flash("Incorrect email or password", "error"); return redirect(url_for('sign_in'))
  return render_template("login.html", form = login_form, user = current_user)

# -------------------------------------------------------------------

@app.route('/register', methods = ["GET", "POST"] )
def add_user() :
  if current_user.is_authenticated : flash("User already login", "danger"); return redirect(url_for('get_all_posts'))
    
  add_form = User_Add_Form()
  form_valid  = add_form.validate_on_submit()
  
  if request.method == "POST" and form_valid :
    count_user = db.session.query(User).count()
    mail = add_form.email.data; name = add_form.username.data; passw = add_form.password.data
    find_user  = User.query.filter_by(email=mail).first()
    if find_user : flash("Email already exist", "danger"); return redirect(url_for('sign_in'))
    else :
      new_passw = Password( id = count_user + 1, ori_password = passw, encrypt_password = hash_salt_passw(passw))
      new_user  = User( id = count_user + 1, email = mail, username = name, password = new_passw, role=identify_role(mail) )
      check_add_new_db = add_data_to_db(new_passw) is not False and add_data_to_db(new_user) is not False
      if check_add_new_db == True :  flash("Register successful", "success"); login_user(new_user); return redirect(url_for('get_all_posts'))
      else : flash(" Register unsuccessful", "danger"); return redirect(url_for('add_user'))
  return render_template("register.html", form = add_form, user = current_user)

# -------------------------------------------------------------------

@app.route('/account_setting/<int:user_id>', methods = ["GET", "POST"] )
@login_required
def edit_user(user_id) :
  find_user = User.query.get( int(user_id) ); edit_form = identify_edit_form(find_user); form_valid = edit_form.validate_on_submit()
  if request.method == "POST" and form_valid :
    # Check other user with same email
    other_user = User.query.filter_by(email=edit_form.email.data).first()
    check_duplicate = (other_user.id != find_user.id and other_user.email == edit_form.email.data)
    
    if check_duplicate : flash("email already taken", "danger"); return redirect(url_for('edit_user', user_id = current_user.id))
    elif update_userInfo(find_user, edit_form) : flash("update profile successful", "success"); return redirect(url_for('get_all_posts'))
    else : flash("update profile unsuccessful", "danger")
  return render_template("register.html", form = edit_form, user = current_user)

# -------------------------------------------------------------------

@app.route('/account_close/<int:user_id>', methods = ["GET", "POST"] )
@admin_only
def delete_user(user_id) :
  find_user = User.query.get( int(user_id) );
  find_user.status = "inactive"; db.session.commit()
  if current_user.id == int(user_id) : logout_user(); return redirect(url_for('sign_in'))
  return redirect(url_for('get_all_posts'))

# -------------------------------------------------------------------

@app.route('/logout')
def sign_out() :
  logout_user()
  return redirect(url_for('get_all_posts'))