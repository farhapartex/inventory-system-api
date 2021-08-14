from inventory.config.base import *

SECRET_KEY = settings_json.get("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASE = settings_json.get("DATABASE", {})
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # 'django.db.backends.mysql',
        'NAME': DATABASE.get("name", ""),
        'USER': DATABASE.get("user", ""),
        'PASSWORD': DATABASE.get("password", ""),
        'HOST': DATABASE.get("host", ""),
        'PORT': DATABASE.get("port", "")
    }
}