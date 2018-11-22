from __future__ import unicode_literals

SECRET_KEY = 'not-anymore'

TIME_ZONE = 'America/Chicago'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = [
    'tests',
]

SILENCED_SYSTEM_CHECKS = []
