"""
This is the settings file used in production.
First, it imports all default settings, then overrides respective ones.
Secrets are stored in and imported from an additional file, not set under version control.
"""

from pyticket import settings_secrets as secrets

from .settings import *

SECRET_KEY = secrets.SECRET_KEY

DEBUG = False

ALLOWED_HOSTS = ['.fachschaft.informatik.tu-darmstadt.de', '.d120.de']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'pyticket',
        'USER': 'pyticket',
        'PASSWORD': secrets.DB_PASSWORD,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'isolation_level': "repeatable read"
        }
    }
}

STATIC_URL = '/pyticket/static/'


SERVER_EMAIL = "pyticket@fachschaft.informatik.tu-darmstadt.de"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.d120.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pyticket'
EMAIL_HOST_PASSWORD = secrets.MAIL_PASSWORD

