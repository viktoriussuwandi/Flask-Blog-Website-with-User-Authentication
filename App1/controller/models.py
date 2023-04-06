from App1 import app, db
from flask_login import UserMixin
# from sqlalchemy.orm import relationship

##CONFIGURE TABLES
class BlogPost(db.Model):
  __tablename__ = "blog_posts"
  id       = db.Column(db.Integer, primary_key=True)
  author   = db.Column(db.String(250), nullable=False)
  title    = db.Column(db.String(250), unique=True, nullable=False)
  subtitle = db.Column(db.String(250), nullable=False)
  date     = db.Column(db.String(250), nullable=False)
  body     = db.Column(db.Text, nullable=False)
  img_url  = db.Column(db.String(250), nullable=False)
  
  def __repr__(self) : return '<BlogPost {self.title}>'
  def to_dict(self)  : return {col.name : getattr(self, col.name) for col in self.__table__.columns}

class User(UserMixin, db.Model) :
  id       = db.Column(db.Integer, primary_key=True)
  name     = db.Column(db.String(250), nullable=False)
  email    = db.Column(db.String(250), unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)
  
  def __repr__(self) : return '<User {self.title}>'
  def to_dict(self)  : return {col.name : getattr(self, col.name) for col in self.__table__.columns}
    
with app.app_context() : 
  db.create_all()