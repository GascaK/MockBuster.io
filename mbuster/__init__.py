import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///buster.db"
app.config['SECRET_KEY'] = os.environ.get('vquest_secret')
if(app.config['SECRET_KEY'] == None):
    print("Secret Key not set!")

db = SQLAlchemy(app)

from mbuster import routes