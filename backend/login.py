from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, current_user, login_manager, LoginManager
import os

app = Flask(__name__, template_folder='../templates')
bycrypt = Bcrypt(app)
SECRET_KEY = os.urandom(32)
app.config['SERCRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
csrf.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
@login_manager.user_loder

def load_user(user_id):
    return User.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id_no = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String[35], unique=True, nullable=False)
    email = db.Column(db.String[50], unique=True, nullable=False)
    password = db.Column(db.String[35], unique=True, nullable=False)

