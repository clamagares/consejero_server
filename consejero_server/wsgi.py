"""
WSGI config for consejero_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'consejero_server.settings'
#from django.core.wsgi import get_wsgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "consejero_server.settings")

#application = get_wsgi_application()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
