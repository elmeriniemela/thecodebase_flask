
import os
import json
import pkg_resources

CONFIG_PATH = pkg_resources.resource_filename('thecodebase', 'config.json')

CONFIG = {}

def cache_config():
    with open(CONFIG_PATH) as f:
        print("Config cached from %s" % CONFIG_PATH)
        CONFIG.update(json.load(f))

if os.path.isfile(CONFIG_PATH):
    cache_config()
else:
    print("Config missing, website not operational")
