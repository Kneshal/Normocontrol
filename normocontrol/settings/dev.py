
import os

from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),  # noqa
        'USER': os.environ.get('DB_USER'),  # noqa
        'PASSWORD': os.environ.get('DB_PASSWORD'),  # noqa
        'HOST': os.environ.get('DB_HOST'),  # noqa
        'PORT': os.environ.get('DB_PORT'),  # noqa
    }
}
