#!/usr/bin/env python3

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") or \
    "sqlite:///" + os.path.join(basedir, "buster.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('vquest_secret')
if(app.config['SECRET_KEY'] == None):
    print("Secret Key not set!")
    quit()

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from mbuster import routes