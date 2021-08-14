from inventory.config.base import *

SECRET_KEY = 'django-insecure-m#3h^xfar_)+g=0$thsb+sztmwp4$*bty_!gg@8r6!0iv(62iq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}