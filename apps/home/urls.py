# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present Geodata.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # The landing page
    path('', views.landing.as_view(), name="landing"),

    # The home page
    # path('dashboard', views.index.as_view(), name="home"),

    #project urls
    path('project', views.project.as_view(), name="project"),
    path('project/add', views.AddProject.as_view(), name="add-project"),
    path('project/edit/<id>', views.EditProject.as_view(), name="edit-project"),
    path('project/delete/<id>', views.DeleteProject.as_view(), name="delete-project"),
    path('project/details/<id>', views.projectDetails.as_view(), name="project-details"),

    path('project/ags/add/<id>', views.AddProjectAGS.as_view(), name="add-project-ags"),
    path('project/ags/edit/<id>', views.EditProjectAGS.as_view(), name="edit-project-ags"),
    path('project/ags/delete/<id>', views.DeleteProjectAGS.as_view(), name="delete-project-ags"),

    #user urls
    path('profile', views.userprofile.as_view(), name="profile"),

    #contact urls
    path('contact', views.contact.as_view(), name="contact"),
    path('contact/delete/<id>', views.DeleteContact.as_view(), name="delete-contact"),

    # chart
    path('project/borehole', views.borehole.as_view(), name='ajax-chart-borehole'),
    path('project/ajax-chart', views.UserChartAjaxApi.as_view(), name='ajax-chart-project'),

    #success
    path('project/success/<id>', views.success.as_view(), name="project-success"),
    path('ags/success/<id>', views.success.as_view(), name="ags-success"),

    # profile
    path('project/profiles', views.ProjectProfile.as_view(), name="profiles"),
    path('project/profileform', views.ProjectProfileForm, name="profileform"),
    path('project/profiles/delete/<id>', views.DeleteProfile.as_view(), name="delete-profile"),
    path('project/profiles/details/<id>/<pid>', views.profileDetails.as_view(), name="profile-details"),

    # profile
    path('tools', views.tools.as_view(), name="tools"),

]
