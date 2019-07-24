#!/usr/bin/python

import sys
import logging
import json
import pkg_resources

from thecodebase import app
from thecodebase import CONFIG

if CONFIG.get('log_file'):
    logging.basicConfig(filename=CONFIG['log_file'], level=logging.INFO)
else:
    logging.basicConfig(stream=sys.stdout)


app.logger.setLevel(logging.INFO)
app.secret_key = CONFIG["secret_key"]
