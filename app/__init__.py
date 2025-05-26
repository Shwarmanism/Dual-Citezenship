from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from database.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view= 'auth.login'
    login_manager.login_message = 'info'

    from app.routes.auth_routes import auth
    from app.routes.form_routes import form_bp

    app.register_blueprint(auth)
    app.register_blueprint(form_bp)

    return app
