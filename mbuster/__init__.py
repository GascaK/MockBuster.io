#!/usr/bin/env python3

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from imdb import IMDb

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") or \
    "sqlite:///" + os.path.join(basedir, "buster.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('vquest_secret')
if(app.config['SECRET_KEY'] == None):
    print("Secret Key not set!")
    quit()

# Mail configuration.
app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'test@gmail.com',
    MAIL_PASSWORD = 'testloltest',
))


# Flask objects.
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
# IMDb object.
ia = IMDb()

from mbuster import routes