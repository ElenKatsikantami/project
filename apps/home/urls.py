# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present Geodata.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # The landing page
    path('', views.landing.as_view(), name="landing"),
    path('blog', views.blog.as_view(), name="blog"),
    path('contactus', views.contactus.as_view(), name="contactus"),

    # The home page
    # path('dashboard', views.index.as_view(), name="home"),

    #project urls
    path('project', views.project.as_view(), name="project"),
    path('project/add', views.AddProject.as_view(), name="add-project"),
    path('project/edit/<id>', views.EditProject.as_view(), name="edit-project"),
    path('project/delete/<id>', views.DeleteProject.as_view(), name="delete-project"),
    path('project/details/<id>', views.projectDetails.as_view(), name="project-details"),
    path('project/section/<id>', views.projectsection.as_view(), name="project-section"),
    path('project/report/<id>', views.projectreport.as_view(), name="project-report"),

    path('project/ags/add/<id>', views.AddProjectAGS.as_view(), name="add-project-ags"),
    path('project/ags/edit/<pid>/<id>', views.EditProjectAGS.as_view(), name="edit-project-ags"),
    path('project/ags/micoredit/<pid>/<id>', views.EditProjectAGSMicro.as_view(), name="edit-project-ags-micro"),
    path('project/ags/table/<pid>/<id>', views.ags_table, name="ags-table"),
    path('project/ags/delete/<pid>/<id>', views.DeleteProjectAGS.as_view(), name="delete-project-ags"),

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
 
    # default profile
    path('project/default/profiles', views.ProjectDefaultProfile.as_view(), name="defaultprofiles"),

    path('project/default/profile/category/add', views.AddProjectDefaultProfileCategory.as_view(), name="add-defaultprofilescategory"),
    path('project/default/profile/category/edit/<id>', views.EditProjectDefaultProfileCategory.as_view(), name="edit-defaultprofilescategory"),
    path('project/default/profile/category/delete/<id>', views.DeleteProjectDefaultProfileCategory.as_view(), name="delete-defaultprofilescategory"),

    path('project/default/profile/add', views.AddProjectDefaultProfile.as_view(), name="add-defaultprofiles"),
    path('project/default/profile/edit/<id>', views.EditProjectDefaultProfile.as_view(), name="edit-defaultprofiles"),
    path('project/default/profile/delete/<id>', views.DeleteProjectDefaultProfile.as_view(), name="delete-defaultprofiles"),
    path('project/generate/default/profile', views.ProjectDefaultProfileForm, name="generate-defaultprofiles"),

    # privacy
    path('policy', views.policy.as_view(), name="policy"),
    
    # tools
    path('tools', views.tools.as_view(), name="tools"),
    path('generaltools', views.generaltools.as_view(), name="generaltools"),
    path('tools/bearingCapacity', views.Bearing, name="bearingCapacity"),
    path('tools/NSPT', views.NsptCorrection.as_view(), name="NSPT"),
    path('tools/RelativeDensity', views.RelativeDensity, name="RelativeDensity"),
    path('tools/FrictionAngle', views.FrictionAngle, name="FrictionAngle"),
    path('tools/AGSToExcel', views.AGSToExcel.as_view(), name="AGSToExcel"),
    path('tools/AGSValidator', views.AGSValidator.as_view(), name="AGSValidator"),
    path('tools/agsfiles', views.agsfiles.as_view(), name='ajax-tools-agsfiles'),
]
