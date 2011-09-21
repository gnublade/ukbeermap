# These are global settings
# We also import settings_local for TWITTER_USERNAME, TWITTER_PASSWORD and MAPS_KEY 

import logging

try:
    from local import *
except ImportError:
    logging.error("Failed to import local.py") 

