from .base import *
# from django.conf import settings
# from . import base


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# DEFAULT_INDEX_TABLESPACE = ''

# DEFAULT_TABLESPACE = ''

# ABSOLUTE_URL_OVERRIDES = {}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }

# DATABASE_ROUTERS = []