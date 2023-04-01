from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy.orm import relationship

from forms import CreatePostForm, RegisterForm, LoginForm

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
import os, pytz, datetime

# -----------------------------------------------------------------
# APP CONFIG
# -----------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['form_token']
ckeditor = CKEditor(app)
Bootstrap(app)

# -----------------------------------------------------------------
# USER CONFIG
# -----------------------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  find_user = User.query.get(int(user_id))
  return find_user
  
# -----------------------------------------------------------------
# DATABASE CONNECTIONS
# -----------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -----------------------------------------------------------------
# TABLE CONFIG
# -----------------------------------------------------------------

def add_data_to_db(new_data) :
  try :
    db.session.add(new_data)
    #Log in and authenticate user after adding details to database.
    # login_user(new_data)
    return db.session.commit()
  except exc.IntegrityError :
    db.session.rollback()
    return False

def hash_salt_passw(passw) :
  new_passw = generate_password_hash(
    passw, 
    method='pbkdf2:sha256', 
    salt_length=8)
  return new_passw

def get_datePost() :
  dt         = datetime.datetime
  # ip_address = request.remote_addr
  timezone   = "Asia/Jakarta"
  myZone     = pytz.timezone(timezone)
  date_post  = dt.now(myZone).strftime("%B %d, %Y")
  return date_post 
  
class BlogPost(db.Model):
  __tablename__ = "blog_posts"
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(250), nullable=False)
  title = db.Column(db.String(250), unique=True, nullable=False)
  subtitle = db.Column(db.String(250), nullable=False)
  date = db.Column(db.String(250), nullable=False)
  body = db.Column(db.Text, nullable=False)
  img_url = db.Column(db.String(250), nullable=False)
  
  def __repr__(self) : return '<BlogPost {self.title}>'
  def to_dict(self) : return {col.name : getattr(self, col.name) for col in self.__table__.columns}

class User(UserMixin, db.Model) :
  __tablename__ = "users"
  id       = db.Column(db.Integer, primary_key=True)
  email    = db.Column(db.String(250), unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)
  username = db.Column(db.String(250), nullable=False)
  
  def __repr__(self) : return '<User {self.title}>'
  def to_dict(self) : return {col.name : getattr(self, col.name) for col in self.__table__.columns}
  
with app.app_context() : db.create_all()

# -----------------------------------------------------------------
# ROUTES & FUNCTIONS - NO DB INVOLVED
# -----------------------------------------------------------------
@app.route("/about")
def about(): return render_template("about.html", logged_in=current_user.is_authenticated)

@app.route("/contact")
def contact(): return render_template("contact.html", logged_in=current_user.is_authenticated) 

# -----------------------------------------------------------------
# ROUTES & FUNCTIONS - POSTS
# -----------------------------------------------------------------
@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    users = db.session.query(User).all()
    return render_template("index.html", all_posts = posts, all_users = users, logged_in=current_user.is_authenticated)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post, logged_in=current_user.is_authenticated)



@app.route("/new-post", methods = ["GET", "POST"])
@login_required
def add_new_post() :
    pform = CreatePostForm()
    date_post  = get_datePost()
    if request.method == 'POST' and pform.validate_on_submit():
      count_post = db.session.query(BlogPost).count()
      new_post   = BlogPost(
        id       = count_post + 1,
        # Dont forget change to current_user
        author   = pform.author.data,
        title    = pform.title.data,
        subtitle = pform.subtitle.data,
        date     = date_post,
        body     = pform.body.data,
        img_url  = pform.img_url.data,
      )
      if add_data_to_db(new_post) is not False : return redirect(url_for("get_all_posts"))
    else : return render_template("make-post.html", form = pform, logged_in=current_user.is_authenticated)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id) :
    find_post  = BlogPost.query.get(post_id)
    edit_form  = CreatePostForm(
      title    = find_post.title,
      subtitle = find_post.subtitle,
      img_url  = find_post.img_url,
      author   = find_post.author,
      body     = find_post.body
    )
    if request.method == 'POST' and edit_form.validate_on_submit():
      find_post.title    = edit_form.title.data
      find_post.subtitle = edit_form.subtitle.data
      find_post.img_url  = edit_form.img_url.data
      find_post.author   = edit_form.author.data
      find_post.body     = edit_form.body.data
      db.session.commit()
      return redirect(url_for("show_post", post_id=find_post.id))
    return render_template("make-post.html", form=edit_form, logged_in=current_user.is_authenticated)



@app.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id) :
    findPost = BlogPost.query.get(post_id)
    db.session.delete(findPost)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# -----------------------------------------------------------------
# ROUTES & FUNCTIONS - USERS
# -----------------------------------------------------------------

@app.route('/register', methods = ["GET", "POST"])
def register() :
  rform = RegisterForm()
  if request.method == 'POST' and rform.validate_on_submit() :
    count_user   = db.session.query(User).count()
    new_user     = User(
        id       = count_user + 1,
        username = rform.username.data,
        email    = rform.email.data,
        password = hash_salt_passw(rform.passw.data)
      )
    if add_data_to_db(new_user) is not False : 
      login_user(new_user); return redirect(url_for("get_all_posts"))
  return render_template("register.html", form = rform, logged_in=current_user.is_authenticated)

@app.route('/delete/<int:user_id>')
@login_required
def delete_user(user_id) :
  findUser = User.query.get(user_id)
  db.session.delete(findUser)

@app.route('/login', methods=["GET", "POST"])
def login() :
  lform = LoginForm()
  if request.method == 'POST' and lform.validate_on_submit() :
    mail  = lform.email.data
    passw = lform.passw.data
    find_user = User.query.filter_by( email=mail ).first()
    if not find_user : 
      redirect(url_for("login"))
    elif not check_password_hash(find_user.password, passw) : 
      redirect(url_for("login"))
    else : login_user(find_user); return redirect(url_for("get_all_posts"))
  elif current_user.is_authenticated : return redirect(url_for("get_all_posts"))
  else : return render_template("login.html", form = lform, logged_in=current_user.is_authenticated)

@app.route('/logout')
@login_required
def logout() : logout_user(); return redirect(url_for('get_all_posts'))

# -----------------------------------------------------------------
# HOST & PORT
# -----------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)

# adding post :
# https://www.income.com.sg/blog/schizophrenia-in-singapore
# https://www.income.com.sg/blog/school-holiday-activities
# https://www.income.com.sg/blog/insurance-for-mental-illness
