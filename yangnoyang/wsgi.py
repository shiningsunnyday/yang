"""
WSGI config for yangnoyang project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yangnoyang.settings')

application = get_wsgi_application()

# to restart gunicorn: sudo kill -HUP `ps -C gunicorn fch -o pid | head -n 1`