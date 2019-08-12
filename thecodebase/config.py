
import logging
import os
import json

logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

CONFIG = {}

def cache_config():
    with open(CONFIG_PATH) as f_obj:
        CONFIG.update(json.load(f_obj))
        logger.info("Config cached from %s", CONFIG_PATH)

if os.path.isfile(CONFIG_PATH):
    cache_config()
else:
    logger.info("Config missing, website not operational")
