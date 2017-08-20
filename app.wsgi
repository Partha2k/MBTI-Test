#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/pi/mbti/")

from FlaskApp import app as application
application.secret_key = 'devK3ys3cur!ty98'