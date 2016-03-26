# Twitter credentials, can be managed at https://apps.twitter.com/app

CONSUMER_KEY = '<consumer_key>'
CONSUMER_SECRET = '<consumer_secret>'
ACCESS_TOKEN_KEY = '<access_token_key>'
ACCESS_TOKEN_SECRET = '<access_token_secret>'

# local_settings.py can be used to override settings in a local environment
# Silently ignored if it doesn't exist
try:
    from local_settings import *
except ImportError:
    pass
