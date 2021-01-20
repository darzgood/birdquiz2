#!venv/Scripts/python

import cgitb
#cgitb.enable()

from wsgiref.handlers import CGIHandler
from app import app
import sys, traceback

import logging
logging.basicConfig(filename='birdquiz.log',level=logging.DEBUG)

if __name__=="__main__":
    try:
        CGIHandler().run(app)
    except:
        logging.info("Failure")
        logging.error(traceback.format_exc())
        traceback.print_exc(file=open("birdquiz.log","a"))
        sys.exit(1)
