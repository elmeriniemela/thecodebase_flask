#!/usr/bin/python
import sys
import os
import logging
import json

from thecodebase import app as application

logging.basicConfig(stream=sys.stderr)

DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(DIR, 'thecodebase', 'credentials.json')) as f:
    KEY = json.load(f)["secret_key"]

application.secret_key = KEY
