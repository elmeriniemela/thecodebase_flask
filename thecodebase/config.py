
import logging
import os
import json
import pkg_resources

logger = logging.getLogger(__name__)

CONFIG_PATH = pkg_resources.resource_filename('thecodebase', 'config.json')

CONFIG = {}

def cache_config():
    with open(CONFIG_PATH) as f_obj:
        CONFIG.update(json.load(f_obj))
        logger.info("Config cached from %s", CONFIG_PATH)

if os.path.isfile(CONFIG_PATH):
    cache_config()
else:
    logger.info("Config missing, website not operational")
