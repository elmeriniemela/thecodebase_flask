#!/usr/bin/python
import os
from logging.config import dictConfig
from .config import CONFIG

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
            'filename': CONFIG.get("log_file"),
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

app.secret_key = CONFIG["secret_key"]
