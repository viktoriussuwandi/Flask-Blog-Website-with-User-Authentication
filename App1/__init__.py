import os
from flask            import Flask
from flask_bootstrap  import Bootstrap
from flask_ckeditor   import CKEditor
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SECRET_KEY']                     = os.environ['form_token']
app.config['SQLALCHEMY_DATABASE_URI']        = os.environ['db_name']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from App1.routes import crud_post,crud_user, no_crud