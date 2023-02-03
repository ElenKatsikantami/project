# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present Geodata.us
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geodata.settings')

application = get_asgi_application()
