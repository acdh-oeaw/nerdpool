from .base import *
import os

SECRET_KEY = os.environ.get("NP_SECRET_KEY"),

DEBUG = True


ALLOWED_HOSTS = ["127.0.0.1", "localhost" "pd.sisyphos.arz.oeaw.ac.at"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("NP_DB_NAME"),
        "USER": os.environ.get("NP_DB_USER"),
        "PASSWORD": os.environ.get("NP_DB_PASSWORD", None),
        "HOST": os.environ.get("NP_DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("NP_DB_PORT", "5432"),
    }
}


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
