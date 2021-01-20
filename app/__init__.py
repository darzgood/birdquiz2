#!venv/Scripts/python

import sys

saveerr = sys.stderr
saveout = sys.stdout
log = open('birdquiz.log', 'a')
sys.stdout = log
sys.stderr = log

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__))


from app import views, models
from app import DataHandler as DH


sys.stdout = saveout
sys.stderr = saveerr
log.close()
