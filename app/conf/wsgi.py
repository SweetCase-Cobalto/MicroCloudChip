"""
WSGI config for conf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

application = get_wsgi_application()

# Booting Code
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from app.models import User

# 처음 시작용
if len(User.objects.all()) == 0:
    admin = User(userId="admin", pswd="admin")
    admin.save()