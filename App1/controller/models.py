from App1 import db, app

from sqlalchemy.orm import relationship
from flask_login import UserMixin

##CONFIGURE TABLES

# ------------------------------------------------------------------
# User
# ------------------------------------------------------------------
@app.login_manager.user_loader
def load_user(user_id):
  find_user = User.query.get(int(user_id))
  return find_user
  
class User(UserMixin, db.Model) :
  __tablename__    = "users"
  id               = db.Column(db.Integer, primary_key=True, unique=True)
  username         = db.Column(db.String(250), nullable=False)
  email            = db.Column(db.String(250), unique=True, nullable=False)
  role             = db.Column(db.String(50), nullable=False, default="user")
  status           = db.Column(db.String(50), nullable=False, default="active")

  # one to one relationship
  password_id      = db.Column(db.Integer, db.ForeignKey("passwords.id"))
  password         = relationship("Password", backref=db.backref("users", uselist=False)) 
  # one to many relationship
  posts            = relationship("BlogPost", back_populates="user")
  comments         = relationship("Comment",  back_populates="user")
  
  def __repr__(self) : return '<User {self.title}>'
  def to_dict(self)  : 
    return {col.name : getattr(self, col.name) for col in self.__table__.columns}

# ------------------------------------------------------------------
# Password
# ------------------------------------------------------------------
class Password(db.Model) :
  __tablename__    = "passwords"
  id               = db.Column(db.Integer, primary_key=True, unique=True)
  ori_password     = db.Column(db.String(250), nullable=False)
  encrypt_password = db.Column(db.String(250), nullable=False)

  def __repr__(self) : return '<Password {self.title}>'
  def to_dict(self)  : 
    return {col.name : getattr(self, col.name) for col in self.__table__.columns}

# ------------------------------------------------------------------
# Comments
# ------------------------------------------------------------------
class Comment(db.Model) :
  __tablename__    = "comments"
  id               = db.Column(db.Integer, primary_key=True, unique=True)
  text             = db.Column(db.String(250), nullable=False)  
  
# one to many relationship
  user_id          = db.Column(db.Integer, db.ForeignKey("users.id"))
  user             = relationship("User", back_populates="comments")
  def __repr__(self) : return '<Comment {self.title}>'
  def to_dict(self)  : 
    return {col.name : getattr(self, col.name) for col in self.__table__.columns}
    
# ------------------------------------------------------------------
# BlogPost
# ------------------------------------------------------------------
class BlogPost(db.Model) :
  __tablename__    = "blog_posts"
  id               = db.Column(db.Integer, primary_key=True, unique=True)
  author           = db.Column(db.String(250), nullable=False)
  title            = db.Column(db.String(250), unique=True, nullable=False)
  subtitle         = db.Column(db.String(250), nullable=False)
  date             = db.Column(db.String(250), nullable=False)
  body             = db.Column(db.Text, nullable=False)
  img_url          = db.Column(db.String(250), nullable=False)

  # one to many relationship
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
  user = relationship("User", back_populates="posts")

  def __repr__(self) : return '<BlogPost {self.title}>'
  def to_dict(self)  : 
    return {col.name : getattr(self, col.name) for col in self.__table__.columns}
    
with app.app_context() : 
  db.create_all()