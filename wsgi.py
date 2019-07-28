#!/usr/bin/python
import os
from logging.config import dictConfig

if os.environ.get('FLASK_ENV') == 'development':
    handlers = {
        'wsgi': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    }
else:
    handlers = {
        'wsgi': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/uwsgi/thecodebase-flask.log',
            'formatter': 'default',
            'maxBytes': 1024*1000,
            'backupCount': 3
        }
    }


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': handlers,
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})



from thecodebase import app
from thecodebase.config import CONFIG


app.secret_key = CONFIG["secret_key"]
