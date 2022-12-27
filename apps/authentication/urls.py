# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", user_list.as_view(), name="user_list"),
    path("user/edit/<id>", edit_user.as_view(), name="edit-user"),
    path('user/delete/<id>', delete_user.as_view(), name="delete-user"),
]
