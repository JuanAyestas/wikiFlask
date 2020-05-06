from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from palawiki.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(Config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)
  
  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  mail.init_app(app)
  
  from palawiki.users.routes import users
  from palawiki.champions.routes import champions
  from palawiki.main.routes import main
  from palawiki.errors.handlers import errors
  app.register_blueprint(users)
  app.register_blueprint(champions)
  app.register_blueprint(main)
  app.register_blueprint(errors)
  
  return app
