from .base import *

SECRET_KEY = '1'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

OAUTH_EVEONLINE_KEY = ''
OAUTH_EVEONLINE_SECRET = ''
OAUTH_EVEONLINE_CALLBACK = '127.0.0.1:8000/callback'

DISCORD_BOT_SECRET = ''

ASHIMMU_SITE_NAME = 'Ashimmu'

# The server ID should be a string!
DISCORD_SERVER_ID = '0'
