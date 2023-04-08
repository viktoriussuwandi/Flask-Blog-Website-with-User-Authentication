import os, pytz, datetime

from flask              import Flask, abort
from flask_bootstrap    import Bootstrap
from flask_ckeditor     import CKEditor
from flask_sqlalchemy   import SQLAlchemy
from werkzeug.security  import generate_password_hash, check_password_hash
from flask_login        import LoginManager, current_user
from sqlalchemy         import exc
from functools          import wraps

app = Flask(__name__)
login_manager = LoginManager(app)
ckeditor = CKEditor(app)
Bootstrap(app)
# login_manager.init_app(app)

##CONNECT TO DB
app.config['SECRET_KEY']                     = os.environ['form_token']
app.config['SQLALCHEMY_DATABASE_URI']        = os.environ['db_name']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ------------------------------------------------------------------
# Additional Functions
# ------------------------------------------------------------------
def add_Post_to_db(new_row) :
  try :
    db.session.add(new_row); return db.session.commit()
  except exc.IntegrityError :
    db.session.rollback(); return False

def get_datePost() :
  dt         = datetime.datetime
  # ip_address = request.remote_addr
  timezone   = "Asia/Jakarta"
  myZone     = pytz.timezone(timezone)
  date_post  = dt.now(myZone).strftime("%B %d, %Y")
  return date_post 

# ------------------------------------------------------------------
def hash_salt_passw(passw) :
  new_passw = generate_password_hash(
    passw,
    method      = os.environ['security_method'],
    salt_length = int(os.environ['security_length']))
  return new_passw

def check_password(db_passw, input_passw) : return check_password_hash(db_passw, input_passw)

# ------------------------------------------------------------------
def user_only(funct) :
  @wraps(funct)
  def check_is_user(*args, **kwargs) :
    checkings = (current_user.is_authenticated and current_user.status == "active")
    return abort(403) if not checkings else funct(*args, **kwargs)
  return check_is_user

def admin_only(funct) :
  @wraps(funct)
  def check_is_admin(*args, **kwargs) : 
    checkings = (current_user.is_authenticated and current_user.email.split("@")[1] == "admin.com") 
    return abort(403) if not checkings else funct(*args, **kwargs)
  return check_is_admin
  
# ------------------------------------------------------------------
# Continue
# ------------------------------------------------------------------
from App1.routes import crud_post,crud_user, no_crud