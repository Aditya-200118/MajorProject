# from cs50.sql import SQL
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
DB = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()