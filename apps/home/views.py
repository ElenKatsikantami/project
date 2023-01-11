import os
import json
import re
import pyproj
import pandas as pd
import numpy as np
from django.shortcuts import get_object_or_404, redirect, reverse, HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from . ags import AGS
from . utils import util
from . models import ProjectTable, ProjectAGS, ContactTable
from . forms import ProjectForm, ProjectAGSForm, ContactForm
from . ags_reference import ags_reference

chart_list = {
    "factual": [*ags_reference],
    "interpreted": [
        'N SPT Vs Elevation'
        ]}


class landing(CreateView):
    """landing class"""
    template_name = "pages/landing.html"
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        """get context data"""
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Contact request success. Will be in touch soon')
        return redirect(reverse("landing"))


class index(LoginRequiredMixin, TemplateView):
    """Index class"""
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        """get context data"""
        context = super().get_context_data(**kwargs)
        context["projects"] = ProjectTable.objects.filter(
            is_deleted=False).order_by('id')
        return context


class project(LoginRequiredMixin, TemplateView):
    """Project Class"""
    template_name = "pages/project/index.html"

    def get_context_data(self, **kwargs):
        """"get context data"""
        context = super().get_context_data(**kwargs)
        context["projects"] = ProjectTable.objects.filter(
            is_deleted=False).order_by('id')
        return context


class AddProject(LoginRequiredMixin, CreateView):
    """add project"""
    template_name = 'pages/project/form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        project_form = form.save(commit=False)  # the bet isn't saved just yet
        project_form.owner = self.request.user  # you add the user here
        project_form.save()
        return redirect(reverse("project"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditProject(LoginRequiredMixin, UpdateView):
    template_name = 'pages/project/form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        form.save(commit=True)
        return redirect(reverse("project"))

    def get_object(self):
        return get_object_or_404(ProjectTable, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteProject(LoginRequiredMixin, DeleteView):
    model = ProjectTable
    success_url = "/project"
    template_name = "pages/project/delete.html"

    def get_object(self):
        return get_object_or_404(ProjectTable, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class projectDetails(LoginRequiredMixin, TemplateView):
    """Project Class"""
    template_name = "pages/project/details.html"

    def get_context_data(self, **kwargs):
        """"get context data"""
        ags_list, holetable, nspt = [], [], {}
        context = super().get_context_data(**kwargs)
        context["project"] = get_object_or_404(
            ProjectTable, pk=self.kwargs["id"])
        agsfile = ProjectAGS.objects.filter(project_id=self.kwargs["id"])
        geojson_collection = {}
        for ags in agsfile:
            tables = None
            geojson = {"type": "FeatureCollection", "features": []}
            try:
                ags_file_path = os.path.join(
                    settings.MEDIA_ROOT, str(ags.ags_file))
                ags_class = AGS(ags_file=ags_file_path)
                tables, headings = ags_class.ags_to_dataframe()
                util_class = util(tables=tables)
                chart_list['factual']  = util_class.get_chart_list_base_on_ags(headings)
                context["headings"] = json.dumps(chart_list)
                region = " ".join(tables["PROJ"]["PROJ_LOC"])
                proj_code = ags_class.get_proj_code(region=region)
                proj_code_to_wgs = pyproj.Transformer.from_crs(proj_code, 4326)
                if ags_class.ags_version == 'ags3':
                    loca = tables['HOLE']
                if ags_class.ags_version == 'ags4':
                    loca = tables['LOCA']
                util_class.get_geojson(
                    loca, ags, proj_code_to_wgs, holetable, geojson)

            except Exception as exp:
                print(str(exp))
            if tables:
                ags_dict = {}
                ags_name = ags.ags_file.name.split('/')[-1].split('_')[0]
                ags_dict['name'] = ags_name
                ags_dict['id'] = ags.id
                ags_dict['path'] = ags.ags_file
                ags_list.append(ags_dict)
                geojson_collection[ags_name] = geojson
        context["agsfile"] = ags_list
        context["hole"] = json.dumps(geojson_collection)
        context["holetable"] = holetable
        context["nspt"] = json.dumps(nspt)
        return context


class AddProjectAGS(LoginRequiredMixin, CreateView):
    """add project"""
    template_name = 'pages/project/agcform.html'
    form_class = ProjectAGSForm
    error_message = "Invalid AGS File. Standard file is AGS4 format"

    def form_valid(self, form):
        project_ags_form = form.save(commit=False)
        project_ags_form.project = ProjectTable(id=self.kwargs["id"])
        project_ags_form.save()
        return redirect(reverse("project"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditProjectAGS(LoginRequiredMixin, UpdateView):
    template_name = 'pages/project/form.html'
    form_class = ProjectAGSForm

    def form_valid(self, form):
        form.save(commit=True)
        return redirect(reverse("project"))

    def get_object(self):
        return get_object_or_404(ProjectAGS, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteProjectAGS(LoginRequiredMixin, DeleteView):
    model = ProjectTable
    success_url = "/project"
    template_name = "pages/project/delete.html"

    def get_object(self):
        return get_object_or_404(ProjectAGS, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class userprofile(LoginRequiredMixin, TemplateView):
    """Project Class"""
    template_name = "pages/user/profile.html"

    def get_context_data(self, **kwargs):
        """"get context data"""
        context = super().get_context_data(**kwargs)
        return context


class contact(LoginRequiredMixin, TemplateView):
    """contact Class"""
    template_name = "pages/contact/index.html"

    def get_context_data(self, **kwargs):
        """"get context data"""
        context = super().get_context_data(**kwargs)
        context["contacts"] = ContactTable.objects.filter(
            is_deleted=False).order_by('id')
        return context


class DeleteContact(LoginRequiredMixin, DeleteView):
    model = ContactTable
    success_url = "/contact"
    template_name = "pages/contact/delete.html"

    def get_object(self):
        return get_object_or_404(ContactTable, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserChartAjaxApi(View):
    """user based chart"""

    def get(self, request):
        ags_id = self.request.GET.get('ags')
        v1 = self.request.GET.get('v1')
        v2 = self.request.GET.get('v2')
        classtype = self.request.GET.get('classtype')
        chart = self.request.GET.get('chart')
        try:
            agsfile = ProjectAGS.objects.filter(id=ags_id)
            for ags in agsfile:
                ags_file_path = os.path.join(
                    settings.MEDIA_ROOT, str(ags.ags_file))
                ags_class = AGS(ags_file=ags_file_path)
                tables, _ = ags_class.ags_to_dataframe()
                util_class = util(tables=tables)
                # import pdb; pdb.set_trace() #breakpoint  c n s q l
                if v1 == 'Particle Size':
                    result = util_class.get_factual_chart_partical(v1,classtype)
                else:
                    result = util_class.get_factual_chart_data(v1,variable_two=v2, class_type=classtype)
            response_data = {'chart_data': result}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        except Exception as exp:
            response_data = {'chart_data': 'False'}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

class borehole(View):
    """user based chart"""

    def get(self, request):
        ags_id = self.request.GET.get('ags')
        try:
            agsfile = ProjectAGS.objects.filter(id=ags_id)
            for ags in agsfile:
                ags_file_path = os.path.join(
                    settings.MEDIA_ROOT, str(ags.ags_file))
                ags_class = AGS(ags_file=ags_file_path)
                tables, _ = ags_class.ags_to_dataframe()
                util_class = util(tables=tables)
                result = util_class.get_borehole_list_base_on_ags()
            response_data = {'boreholes': result}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        except Exception as exp:
            response_data = {'boreholes': 'False'}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
