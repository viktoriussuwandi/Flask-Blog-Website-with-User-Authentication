from flask            import Flask
from flask_bootstrap  import Bootstrap
from flask_ckeditor   import CKEditor
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from App1.routes import routes_post, routes_user