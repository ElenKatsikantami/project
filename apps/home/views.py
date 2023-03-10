import os
import json
import pyproj
from django.shortcuts import get_object_or_404, redirect, reverse, HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from . ags import AGS
from . utils import util
from . models import ProjectTable, ProjectAGS, ContactTable, Projectprofile, Projectdefaultprofilecategory, Projectdefaultprofile
from . forms import ProjectForm, ProjectAGSForm, ContactForm, ProfileDefaultCategoryForm, ProfileDefaultForm, ProjectEXCELForm

from . ags_reference import ags_reference
from . Bearing_Capacity_for_Shallow_Foundation import *
from . activate_nspt import activate_nspt
from . activate_relativeDensity import *
from django.shortcuts import render

chart_list = {
    "factual": [],
    "interpreted": [
        '(N1)60 Vs Elevation'
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
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["projects"] = ProjectTable.objects.filter(
            is_deleted=False).order_by('id').filter(owner=user)
        return context

class AddProject(LoginRequiredMixin, CreateView):
    """add project"""
    template_name = 'pages/project/form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        project_form = form.save(commit=False)  # the bet isn't saved just yet
        project_form.owner = self.request.user  # you add the user here
        project_form.save()
        messages.success(
            self.request, 'Project added successfully.')
        return HttpResponseRedirect(reverse('project-success', kwargs={'id':1}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditProject(LoginRequiredMixin, UpdateView):
    template_name = 'pages/project/form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Project Edited successfully.')
        return HttpResponseRedirect(reverse('project-success', kwargs={'id':1}))

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
        project = ProjectTable.objects.get(id=self.kwargs["id"])
        context["name"] = project.name
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
                chart_list['factual'],chart_list['interpretation']  = util_class.get_chart_list_base_on_ags(headings)
                context["headings"] = json.dumps(chart_list)
                region = " ".join(tables["PROJ"]["PROJ_LOC"])
                proj_code = ags_class.get_proj_code(region=region)
                proj_code_to_wgs = pyproj.Transformer.from_crs(proj_code, 4326)
                if ags_class.ags_version == 'ags3':
                    loca = tables['HOLE']
                if ags_class.ags_version == 'ags4':
                    # import pdb; pdb.set_trace() #breakpoint  c n s q l
                    df_loca = tables['LOCA']
                    df_mond = tables['MOND']
                    loca = df_loca.merge(
                            df_mond, on='LOCA_ID', how='left')
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
                ags_dict['pid'] = self.kwargs["id"]
                ags_list.append(ags_dict)
                geojson_collection[ags_name] = geojson
        context["agsfile"] = ags_list
        context["hole"] = json.dumps(geojson_collection)
        context["holetable"] = holetable
        context["nspt"] = json.dumps(nspt)
        return context

class projectsection(LoginRequiredMixin, TemplateView):
    """Project Class"""
    template_name = "pages/project/section.html"

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
                chart_list['factual'],chart_list['interpretation']  = util_class.get_chart_list_base_on_ags(headings)
                context["headings"] = json.dumps(chart_list)
                region = " ".join(tables["PROJ"]["PROJ_LOC"])
                proj_code = ags_class.get_proj_code(region=region)
                proj_code_to_wgs = pyproj.Transformer.from_crs(proj_code, 4326)
                if ags_class.ags_version == 'ags3':
                    loca = tables['HOLE']
                if ags_class.ags_version == 'ags4':
                    # import pdb; pdb.set_trace() #breakpoint  c n s q l
                    df_loca = tables['LOCA']
                    df_mond = tables['MOND']
                    loca = df_loca.merge(
                            df_mond, on='LOCA_ID', how='left')
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
                ags_dict['pid'] = self.kwargs["id"]
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
        messages.success(
            self.request, 'AGS file added successfully.')
        return HttpResponseRedirect(reverse('ags-success', kwargs={'id':self.kwargs["id"]}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditProjectAGS(LoginRequiredMixin, UpdateView):
    template_name = 'pages/project/form.html'
    form_class = ProjectAGSForm

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Project AGS file edited successfully.')
        return HttpResponseRedirect(reverse('ags-success', kwargs={'id':self.kwargs["pid"]}))

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
        ags = ProjectAGS.objects.get(id=self.kwargs["id"])
        agsname = ags.ags_file.name.split('/')[-1].split('_')[0]
        context["project"] = ags.project.name
        context["name"] = agsname
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
                elif v1 == 'Water Level':
                    result = util_class.get_factual_chart_waterlevel(v2)
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

class success(LoginRequiredMixin, TemplateView):
    """success class"""
    template_name = "pages/success.html"
    
    def get_context_data(self, **kwargs):
        """get context data"""
        context = super().get_context_data(**kwargs)
        context["project"] = self.kwargs["id"]
        return context

class ProjectProfile(LoginRequiredMixin, TemplateView):
    """Project Class"""
    template_name = "pages/profile/index.html"

    def get_context_data(self, **kwargs):
        """"get context data"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["profiles"] = Projectprofile.objects.order_by('id').filter(project__owner=user)
        return context

def ProjectProfileForm(request):
    """project profile form addition"""
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            projectid = request.POST.get('project')
            chart = request.POST.get('chart')
            # import pdb; pdb.set_trace() #breakpoint  c n s q l
            project = ProjectTable.objects.get(id=projectid)
            p = Projectprofile(name=name, project=project, chart=json.loads(chart), type='Custom')
            p.save()
            result = {'message': 'Profile added successfully'}
        else:
            result = {'message': 'Oops there is some error'}
    except Exception as e:
        result = {'message': 'Oops there is some error. Try Again' + str(e)}
        return HttpResponse(json.dumps(result), content_type='application/json')
    return HttpResponse(json.dumps(result), content_type='application/json')

class DeleteProfile(LoginRequiredMixin, DeleteView):
    model = ProjectTable
    success_url = "/project/profiles"
    template_name = "pages/profile/delete.html"

    def get_object(self):
        return get_object_or_404(Projectprofile, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prf = Projectprofile.objects.get(id=self.kwargs["id"])
        prfname = prf.name
        context["project"] = prf.project.name
        context["name"] = prfname
        return context

class profileDetails(LoginRequiredMixin, TemplateView):
    """Project Class"""
    template_name = "pages/profile/details.html"

    def get_context_data(self, **kwargs):
        """"get context data"""
        ags_list, holetable, nspt = [], [], {}
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(
            Projectprofile, pk=self.kwargs["pid"])
        context["profile"] = profile
        # import pdb; pdb.set_trace() #breakpoint  c n s q l
        context["chartjson"] = json.dumps(profile.chart)
        chartlist = [*profile.chart]
        context["chartlist"] = json.dumps(chartlist)
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
                chart_list['factual'],chart_list['interpretation']  = util_class.get_chart_list_base_on_ags(headings)
                context["headings"] = json.dumps(chart_list)
                region = " ".join(tables["PROJ"]["PROJ_LOC"])
                proj_code = ags_class.get_proj_code(region=region)
                proj_code_to_wgs = pyproj.Transformer.from_crs(proj_code, 4326)
                if ags_class.ags_version == 'ags3':
                    loca = tables['HOLE']
                if ags_class.ags_version == 'ags4':
                    # import pdb; pdb.set_trace() #breakpoint  c n s q l
                    df_loca = tables['LOCA']
                    df_mond = tables['MOND']
                    loca = df_loca.merge(
                            df_mond, on='LOCA_ID', how='left')
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

class tools(LoginRequiredMixin, TemplateView):
    """tools Class"""
    template_name = "pages/tool/index.html"

    def get_context_data(self, **kwargs):
        """"get context data"""
        NSPT_activated = []
        for ags in ProjectAGS.objects.all().filter(nspt_activated=True):
            project = ProjectTable.objects.get(id=ags.project_id).name
            ags_name = ags.ags_file.name.split("/")[-1]
            NSPT_activated.append((project,ags_name))
            
        Skempton_activated = []
        for ags in ProjectAGS.objects.all().filter(rdSkempton_activated=True):
            project = ProjectTable.objects.get(id=ags.project_id).name
            ags_name = ags.ags_file.name.split("/")[-1]
            Skempton_activated.append((project,ags_name))
        
        Terzaghi_activated = []
        for ags in ProjectAGS.objects.all().filter(rdTerzaghi_activated=True):
            project = ProjectTable.objects.get(id=ags.project_id).name
            ags_name = ags.ags_file.name.split("/")[-1]
            Terzaghi_activated.append((project,ags_name))
        RelativeDensityALL = set(Skempton_activated + Terzaghi_activated)
        RelativeDensity_activated = []
        for i in RelativeDensityALL:
            if i in Skempton_activated and i in Terzaghi_activated:
                RelativeDensity_activated.append(("both",)+i)
            elif i in Skempton_activated and i not in Terzaghi_activated:
                RelativeDensity_activated.append(("Skempton",)+i)
            else:
                RelativeDensity_activated.append(("Terzaghi and Peck",)+i)
        context = super().get_context_data(**kwargs)
        context["nspt_activated"] = NSPT_activated
        context["RelativeDensity_activated"] = RelativeDensity_activated
        return context


class ProjectDefaultProfile(LoginRequiredMixin, TemplateView):
    """Project Default profile Class"""
    template_name = "pages/profile/default/index.html"

    def get_context_data(self, **kwargs):
        """"get context data"""
        context = super().get_context_data(**kwargs)
        context["category"] = Projectdefaultprofilecategory.objects.order_by('id')
        context["defaultprofile"] = Projectdefaultprofile.objects.order_by('id')
        return context

class AddProjectDefaultProfileCategory(LoginRequiredMixin, CreateView):
    """add project Default profile category"""
    template_name = 'pages/profile/default/form.html'
    form_class = ProfileDefaultCategoryForm
    error_message = "Invalid Category"

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Category added successfully.')
        return redirect(reverse("defaultprofiles"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditProjectDefaultProfileCategory(LoginRequiredMixin, UpdateView):
    template_name = 'pages/profile/default/form.html'
    form_class = ProfileDefaultCategoryForm

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Category edited successfully.')
        return redirect(reverse("defaultprofiles"))

    def get_object(self):
        return get_object_or_404(Projectdefaultprofilecategory, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DeleteProjectDefaultProfileCategory(LoginRequiredMixin, DeleteView):
    model = Projectdefaultprofilecategory
    success_url = "/project/default/profiles"
    template_name = "pages/profile/default/delete.html"

    def get_object(self):
        return get_object_or_404(Projectdefaultprofilecategory, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AddProjectDefaultProfile(LoginRequiredMixin, CreateView):
    """add project Default profile category"""
    template_name = 'pages/profile/default/form.html'
    form_class = ProfileDefaultForm
    error_message = "Invalid Category"

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Category added successfully.')
        return redirect(reverse("defaultprofiles"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditProjectDefaultProfile(LoginRequiredMixin, UpdateView):
    template_name = 'pages/profile/default/form.html'
    form_class = ProfileDefaultForm

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Category edited successfully.')
        return redirect(reverse("defaultprofiles"))

    def get_object(self):
        return get_object_or_404(Projectdefaultprofile, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DeleteProjectDefaultProfile(LoginRequiredMixin, DeleteView):
    model = Projectdefaultprofile
    success_url = "/project/default/profiles"
    template_name = "pages/profile/default/delete.html"

    def get_object(self):
        return get_object_or_404(Projectdefaultprofile, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def ProjectDefaultProfileForm(request):
    """project profile form addition"""
    chartindexChoices = ['First','Second','Third','Fourth','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelveve']
    try:
        if request.method == 'POST':
            # import pdb; pdb.set_trace() #breakpoint  c n s q l
            projectid = request.POST.get('project')
            project = ProjectTable.objects.get(id=projectid)
            agslist = ProjectAGS.objects.filter(project_id=projectid)
            categories = Projectdefaultprofilecategory.objects.order_by('id')
            for category in categories:
                chartdict = {}
                counter = 0
                for ags in agslist:
                    name = category.name
                    defaultprofile = Projectdefaultprofile.objects.filter(category_id=category.id)
                    for profile in defaultprofile:
                        chartinnerdict = {}
                        chartinnerdict['ags'] = ags.id
                        chartinnerdict['v1'] = profile.variable1
                        chartinnerdict['v2'] = profile.variable2
                        chartinnerdict['classtype'] = profile.variable3
                        chartinnerdict['chart'] = 'Scatter'
                        chartinnerdict['ags_text'] = ags.ags_file.name.split('/')[-1].split('_')[0]
                        chartdict["drawChart-"+chartindexChoices[counter].lower()] = chartinnerdict
                        counter+=1
                        if counter == len(chartindexChoices)-1:
                            break
                # import pdb; pdb.set_trace() #breakpoint  c n s q l
                instance = Projectprofile.objects.filter(name=name).filter(is_default=True).filter(project_id=projectid)
                for obj in instance:
                    obj.delete()
                p = Projectprofile(name=name, project=project, chart=chartdict,is_default=True)
                p.save()
            result = {'message': 'Default Profile generated successfully'}
        else:
            result = {'message': 'Oops there is some error'}
    except Exception as e:
        result = {'message': 'Oops there is some error. Try Again' + str(e)}
        return HttpResponse(json.dumps(result), content_type='application/json')
    return HttpResponse(json.dumps(result), content_type='application/json')


def Bearing(request):
    if request.method == "POST":
        Width_of_foundation = float(request.POST["width"])
        Length_of_foundation = float(request.POST["length"])
        Embedment_depth_of_footings = float(request.POST["df"])
        Depth_to_Water = float(request.POST["dw"])
        Friction_Angle = float(request.POST["Friction_Angle"])
        Cohesion = float(request.POST["Cohesion"])
        Unit_Weight = float(request.POST["Unit_Weight"])
        alpha = float(request.POST["alpha"])
        Factor_of_safety = float(request.POST["Factor_of_safety"])
        inputs =[Width_of_foundation,Length_of_foundation,Embedment_depth_of_footings,Depth_to_Water
                ,Friction_Angle,Cohesion,Unit_Weight,alpha,Factor_of_safety]
        method = request.POST["method"]
        if method =="Meyerhof":
            result = get_qallow_Meyerhof(*inputs)
        elif method =="Terzaghi":
            result = get_qallow_Terzaghi(*inputs)
        elif method =="Hansen":
            eta = float(request.POST["eta"])
            beta = float(request.POST["beta"])
            inputs=inputs+[eta,beta]
            result = get_qallow_Hansen(*inputs)  
        else:
            eta = float(request.POST["eta"])
            beta = float(request.POST["beta"])
            inputs=inputs+[eta,beta]
            result = get_qallow_Vesic(*inputs)
        context = {"result":result}
        return render(request,"pages/tool/result.html",context)
    else:
        result=""
    return render(request,"pages/tool/Bearing.html")

class agsfiles(View):
    """AGS file"""
    def get(self, request):
        project_id = self.request.GET.get('project_id')
        agsfile = ProjectAGS.objects.all().filter(project_id=project_id)
        result=[]
        for ags in agsfile:
            if ags.ags_file.name:
                result.append([ags.id,ags.ags_file.name.split("/")[-1]])
        response_data = {'agsfiles': result}
        return HttpResponse(json.dumps(response_data), content_type='application/json')

class NsptCorrection(LoginRequiredMixin, CreateView):
    """add project"""
    template_name = 'pages/tool/NSPT.html'
    form_class = ProjectEXCELForm
    
    def form_valid(self, form):
        project_excel_form = form.save(commit=False)
        project_excel_form.project = ProjectTable(id=self.request.POST["select-variable-first"])

        for ags_id in self.request.POST.getlist("select-variable-second"):
            project_excel_form.ags_file = ProjectAGS(id=ags_id)
            project_excel_form.save()
            ags = ProjectAGS.objects.get(id=ags_id
                        ,project_id=self.request.POST["select-variable-first"])
            ags.nspt_activated = True
            ags.save()
            file_ags =ags.ags_file.path
            cs = float(self.request.POST["CS"])
            method = self.request.POST["CN"]
            maximum = self.request.POST["Maximum"]
            correct = self.request.POST["correct"]
            Efficiency_file = ""
            if self.request.POST["method"] == "excel":
                try:
                    Efficiency_file = project_excel_form.excel_file.path
                    
                except:
                    pass
                response = activate_nspt(file_ags,Efficiency_file,cs,method,maximum,correct) 
            elif self.request.POST["method"] == "excel":
                machines = self.request.POST.getlist("machine")
                response = activate_nspt(file_ags,machines,cs,method,maximum,correct)
            else:
                response = activate_nspt(file_ags,70,cs,method,maximum,correct)
            messages.add_message(self.request,25,response)
            
        return HttpResponseRedirect(reverse('NSPT'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = ProjectTable.objects.all().filter(owner_id = self.request.user.id)
        return context

def RelativeDensity(request):
    """Relative Density"""
    context={}
    context["projects"] = ProjectTable.objects.all().filter(owner_id = request.user.id)
    context["dr"] = ""
    context["class"] = ""
    
    for ags_id in request.POST.getlist("select-variable-second"):
        ags = ProjectAGS.objects.get(
                        id=ags_id
                        ,project_id=request.POST["select-variable-first"])
        
        file_ags =ags.ags_file.path
        method = request.POST["method"]
        if method =="Terzaghi":
            ags.rdTerzaghi_activated = True
            ags.save()
        elif method =="Skempton":
            if ags.nspt_activated:
                ags.rdSkempton_activated = True
                ags.save()
        elif method == "Both":
            ags.rdTerzaghi_activated = True
            if ags.nspt_activated:
                ags.rdSkempton_activated = True
            ags.save()
            
        response = activateRelativeDensity(file_ags,method)

        messages.add_message(request,25,response)
    return render(request,'pages/tool/RelativeDensity.html', context)

class ProjectDefaultProfile(LoginRequiredMixin, TemplateView):
    """Project Default profile Class"""
    template_name = "pages/profile/default/index.html"

    def get_context_data(self, **kwargs):
        """"get context data"""
        context = super().get_context_data(**kwargs)
        context["category"] = Projectdefaultprofilecategory.objects.order_by('id')
        context["defaultprofile"] = Projectdefaultprofile.objects.order_by('id')
        return context

class AddProjectDefaultProfileCategory(LoginRequiredMixin, CreateView):
    """add project Default profile category"""
    template_name = 'pages/profile/default/form.html'
    form_class = ProfileDefaultCategoryForm
    error_message = "Invalid Category"

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Category added successfully.')
        return redirect(reverse("defaultprofiles"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditProjectDefaultProfileCategory(LoginRequiredMixin, UpdateView):
    template_name = 'pages/profile/default/form.html'
    form_class = ProfileDefaultCategoryForm

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Category edited successfully.')
        return redirect(reverse("defaultprofiles"))

    def get_object(self):
        return get_object_or_404(Projectdefaultprofilecategory, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DeleteProjectDefaultProfileCategory(LoginRequiredMixin, DeleteView):
    model = Projectdefaultprofilecategory
    success_url = "/project/default/profiles"
    template_name = "pages/profile/default/delete.html"

    def get_object(self):
        return get_object_or_404(Projectdefaultprofilecategory, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AddProjectDefaultProfile(LoginRequiredMixin, CreateView):
    """add project Default profile category"""
    template_name = 'pages/profile/default/form.html'
    form_class = ProfileDefaultForm
    error_message = "Invalid Category"

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Category added successfully.')
        return redirect(reverse("defaultprofiles"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditProjectDefaultProfile(LoginRequiredMixin, UpdateView):
    template_name = 'pages/profile/default/form.html'
    form_class = ProfileDefaultForm

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(
            self.request, 'Category edited successfully.')
        return redirect(reverse("defaultprofiles"))

    def get_object(self):
        return get_object_or_404(Projectdefaultprofile, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DeleteProjectDefaultProfile(LoginRequiredMixin, DeleteView):
    model = Projectdefaultprofile
    success_url = "/project/default/profiles"
    template_name = "pages/profile/default/delete.html"

    def get_object(self):
        return get_object_or_404(Projectdefaultprofile, pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def ProjectDefaultProfileForm(request):
    """project profile form addition"""
    chartindexChoices = ['First','Second','Third','Fourth','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelveve']
    try:
        if request.method == 'POST':
            # import pdb; pdb.set_trace() #breakpoint  c n s q l
            projectid = request.POST.get('project')
            project = ProjectTable.objects.get(id=projectid)
            agslist = ProjectAGS.objects.filter(project_id=projectid)
            categories = Projectdefaultprofilecategory.objects.order_by('id')
            for category in categories:
                chartdict = {}
                counter = 0
                for ags in agslist:
                    name = category.name
                    defaultprofile = Projectdefaultprofile.objects.filter(category_id=category.id)
                    for profile in defaultprofile:
                        chartinnerdict = {}
                        chartinnerdict['ags'] = ags.id
                        chartinnerdict['v1'] = profile.variable1
                        chartinnerdict['v2'] = profile.variable2
                        chartinnerdict['classtype'] = profile.variable3
                        chartinnerdict['chart'] = 'Scatter'
                        chartinnerdict['ags_text'] = ags.ags_file.name.split('/')[-1].split('_')[0]
                        chartdict["drawChart-"+chartindexChoices[counter].lower()] = chartinnerdict
                        counter+=1
                        if counter == len(chartindexChoices)-1:
                            break
                # import pdb; pdb.set_trace() #breakpoint  c n s q l
                instance = Projectprofile.objects.filter(name=name).filter(is_default=True).filter(project_id=projectid)
                for obj in instance:
                    obj.delete()
                p = Projectprofile(name=name, project=project, chart=chartdict,is_default=True)
                p.save()
            result = {'message': 'Default Profile generated successfully'}
        else:
            result = {'message': 'Oops there is some error'}
    except Exception as e:
        result = {'message': 'Oops there is some error. Try Again' + str(e)}
        return HttpResponse(json.dumps(result), content_type='application/json')
    return HttpResponse(json.dumps(result), content_type='application/json')
