# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present Geodata.us
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geodata.settings')

application = get_wsgi_application()
