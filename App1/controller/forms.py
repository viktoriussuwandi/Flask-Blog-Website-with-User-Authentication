from flask_wtf        import FlaskForm
from flask_ckeditor   import CKEditorField

from wtforms            import StringField, SubmitField,PasswordField, SelectField
from wtforms.validators import DataRequired, URL, Email

from App1.controller.models import User
from fastapi.encoders       import jsonable_encoder

##WTForm
# ---------------------------------------------------------------------------------
class Post_Add_Form(FlaskForm):
  title     = StringField("Blog Post Title", validators=[DataRequired()])
  subtitle  = StringField("Subtitle", validators=[DataRequired()])
  img_url   = StringField("Blog Image URL", validators=[DataRequired(), URL()])
  body      = CKEditorField("Blog Content", validators=[DataRequired()])
  submit    = SubmitField("Post article")

class Post_Edit_Form_As_Admin(FlaskForm):
  emails    = [ u["email"] for u in [ jsonable_encoder(u) for u in User.query.all() ] ]
  status    = SelectField("Status", choices = [('active','active'),('inactive','inactive')] )
  # author    = SelectField("Author mail", choices = [ (m,m) for m in mail_list] )
  title     = StringField("Blog Post Title", validators=[DataRequired()])
  subtitle  = StringField("Subtitle", validators=[DataRequired()])
  img_url   = StringField("Blog Image URL", validators=[DataRequired(), URL()])
  body      = CKEditorField("Blog Content", validators=[DataRequired()])
  submit    = SubmitField("Update Article")

class Post_Edit_Form_As_User(FlaskForm):
  title    = StringField("Blog Post Title", validators=[DataRequired()])
  subtitle = StringField("Subtitle", validators=[DataRequired()])
  img_url  = StringField("Blog Image URL", validators=[DataRequired(), URL()])
  body     = CKEditorField("Blog Content", validators=[DataRequired()])
  submit   = SubmitField("Update Article")

# ---------------------------------------------------------------------------------
class User_Login_Form(FlaskForm) :
  email    = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit   = SubmitField("Login")

class User_Add_Form(FlaskForm) :
  username = StringField("Username", validators=[DataRequired()])
  email    = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit   = SubmitField("Register")

class User_Edit_Form_As_Admin(FlaskForm) :
  username = StringField("Username", validators=[DataRequired()])
  email    = StringField("Email", validators=[DataRequired(), Email()])
  password = StringField("Password", validators=[DataRequired()])
  role     = SelectField("Role",   choices = [('user','user'),('admin','admin')] )
  status   = SelectField("Status", choices = [('active','active'),('inactive','inactive')] )
  submit   = SubmitField("Update User")

class User_Edit_Form_As_User(FlaskForm) :
  username = StringField("Username", validators=[DataRequired()])
  email    = StringField("Email", validators=[DataRequired(), Email()])
  password = StringField("Password", validators=[DataRequired()])
  submit   = SubmitField("Update User")