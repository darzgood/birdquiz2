#!venv/Scripts/python

import sys

saveerr = sys.stderr
saveout = sys.stdout                                     
log = open('birdquiz.log', 'a')               
sys.stdout = log                                       
sys.stderr = log


import os
from app import DataHandler as DH
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WTF_CSRF_ENABLED = True
SECRET_KEY = 'birdquiz'

sys.stdout = saveout
sys.stderr = saveerr                                     
log.close()  

