from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
migrate = Migrate(app, db)

from hashlib import shake_128
app.jinja_env.globals.update(shake_128=lambda x: shake_128(bytes(x, 'utf-8')).hexdigest(len(x)))
# So that Jinja can hash

from app import routes, models
