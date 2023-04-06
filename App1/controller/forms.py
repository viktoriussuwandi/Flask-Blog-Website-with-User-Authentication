from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm):
  title    = StringField("Blog Post Title", validators=[DataRequired()])
  subtitle = StringField("Subtitle", validators=[DataRequired()])
  img_url  = StringField("Blog Image URL", validators=[DataRequired(), URL()])
  body     = CKEditorField("Blog Content", validators=[DataRequired()])
  submit   = SubmitField("Post article")

class LoginForm(FlaskForm) :
  username = StringField("Username", validators=[DataRequired()])
  passw    = PasswordField("Password", validators=[DataRequired()])
  submit   = SubmitField("Login")

class RegisterForm(FlaskForm) :
  username = StringField("Username", validators=[DataRequired()])
  passw    = StringField("Password", validators=[DataRequired()])
  submit   = SubmitField("Login")