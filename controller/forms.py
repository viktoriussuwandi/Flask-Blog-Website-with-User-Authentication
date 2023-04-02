from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

##WTForm
class CommentForm(FlaskForm) :
  body     = CKEditorField("Blog Content",  validators=[DataRequired()] )
  submit   = SubmitField("Submitt")
  
class CreatePostForm(FlaskForm) :
  author   = StringField("Author", render_kw={'readonly': True}, validators=[DataRequired()] )
  title    = StringField("Blog Post Title", validators=[DataRequired()] )
  subtitle = StringField("Subtitle",        validators=[DataRequired()] )
  img_url  = StringField("Blog Image URL",  validators=[DataRequired(), URL()] )
  body     = CKEditorField("Blog Content",  validators=[DataRequired()] )
  submit   = SubmitField("Post")
  
class RegisterForm(FlaskForm) :
  email    = StringField("Email",    validators=[ DataRequired(), Email() ] )
  passw    = StringField("Password", validators=[ DataRequired() ] )
  username = StringField("Username", validators=[ DataRequired() ] )
  submit   = SubmitField("Sign Up")

class LoginForm(FlaskForm) :
  email    = StringField("Email",    validators=[ DataRequired(), Email() ] )
  passw    = StringField("Password", validators=[ DataRequired() ] )
  submit   = SubmitField("Login")
