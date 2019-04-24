"""
This is the settings file used in production.
First, it imports all default settings, then overrides respective ones.
Secrets are stored in and imported from an additional file, not set under version control.
"""

from pyticket import settings_secrets as secrets
import os

from .settings import *

import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion, LDAPGroupQuery, GroupOfNamesType


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
LOGIN_URL = '/pyticket/accounts/login/'
MEDIA_URL = '/pyticket/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SERVER_EMAIL = "pyticket@fachschaft.informatik.tu-darmstadt.de"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.d120.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pyticket'
EMAIL_HOST_PASSWORD = secrets.MAIL_PASSWORD

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend'
]
AUTH_LDAP_SERVER_URI = "ldap://ldap.d120.de"
AUTH_LDAP_BIND_DN = "cn=pyticket,ou=Services,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de"
AUTH_LDAP_BIND_PASSWORD = secrets.AUTH_LDAP_BIND_PASSWORD
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de",
    ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Group,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de",
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
)

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
AUTH_LDAP_MIRROR_GROUPS = True

AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn",
        "email": "mail"}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_staff": "cn=fachschaft,ou=Group,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de",
        "is_superuser": (LDAPGroupQuery("cn=developers,ou=Group,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de") |
                        LDAPGroupQuery("cn=fss,ou=Group,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de"))
}     
