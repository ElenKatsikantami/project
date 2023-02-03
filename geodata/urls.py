# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present Geodata.us
"""

# from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static# add this
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    # path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
