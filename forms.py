from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm) :
  title    = StringField("Blog Post Title", validators=[DataRequired()] )
  subtitle = StringField("Subtitle",        validators=[DataRequired()] )
  author   = StringField("Author",          validators = [ DataRequired() ] )
  img_url  = StringField("Blog Image URL",  validators=[DataRequired(), URL()] )
  body     = CKEditorField("Blog Content",  validators=[DataRequired()] )
  submit   = SubmitField("Submit Post")
  
class RegisterForm(FlaskForm) :
  email    = StringField("Email",    validators=[ DataRequired(), Email() ] )
  passw    = StringField("Password", validators=[ DataRequired() ] )
  username = StringField("Username", validators=[ DataRequired() ] )
  submit   = SubmitField("Sign Up")

class LoginForm(FlaskForm) :
  email    = StringField("Email",    validators=[ DataRequired(), Email() ] )
  passw    = StringField("Password", validators=[ DataRequired() ] )
  submit   = SubmitField("Login")
