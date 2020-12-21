from .base import *
import os

SECRET_KEY = os.environ.get("NP_SECRET_KEY"),

DEBUG = True


ALLOWED_HOSTS = ["127.0.0.1", "localhost" "pd.sisyphos.arz.oeaw.ac.at"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGDATABASE"),
        "USER": os.environ.get("PGUSER"),
        "PASSWORD": os.environ.get("PGPASSWORD", None),
        "HOST": os.environ.get("PGHOST", "127.0.0.1"),
        "PORT": os.environ.get("PGPORT", "5432"),
    }
}


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
