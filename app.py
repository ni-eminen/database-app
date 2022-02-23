from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv

# flask plugins
from flask_login import LoginManager
from flask_cors import CORS
from flask_bootstrap import Bootstrap

# user classes
from database import *

# app object
app = Flask(__name__)
login_manager = LoginManager()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
Bootstrap(app)
login_manager.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

import routes