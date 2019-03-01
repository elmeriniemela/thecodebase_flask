#!/usr/bin/python

import sys
import logging
import json
import pkg_resources

from thecodebase import app as application

logging.basicConfig(stream=sys.stderr)

CONF = pkg_resources.resource_filename('thecodebase', 'credentials.json')
with open(CONF) as f:
    KEY = json.load(f)["secret_key"]

application.secret_key = KEY
