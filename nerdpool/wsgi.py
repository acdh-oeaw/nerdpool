import os
import sys

sys.path.append('/nerdpool/nerdpool')
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nerdpool.settings.server")

application = get_wsgi_application()
