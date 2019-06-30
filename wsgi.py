#!/usr/bin/python

import sys
import logging
import json
import pkg_resources

from thecodebase import app

CONF_FNAME = pkg_resources.resource_filename('thecodebase', 'credentials.json')

with open(CONF_FNAME) as f:
    CONF = json.load(f)

if CONF.get('log_file'):
    logging.basicConfig(filename=CONF['log_file'], level=logging.INFO)
else:
    logging.basicConfig(stream=sys.stdout)


app.logger.setLevel(logging.INFO)
app.secret_key = CONF["secret_key"]
