#!/usr/bin/python
import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'thecodebase'))

from thecodebase import app as application

import json
current_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(current_dir, 'thecodebase', 'credentials.json')) as f:
    secret_key = json.load(f)["secret_key"]

application.secret_key = secret_key
