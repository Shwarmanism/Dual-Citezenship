from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
import os

app = Flask(__name__, template_folder='../templates')
bycrypt = Bcrypt(app)
SECRET_KEY = os.urandom(32)
app.config['SERCRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id_no = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String[35], unique=True, nullable=False)
    email = db.Column(db.String[50], unique=True, nullable=False)
    password = db.Column(db.String[35], unique=True, nullable=False)

