"""forms for home app"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.conf import settings
from .models import ProjectTable,ProjectAGS,ContactTable,Projectprofile, Projectdefaultprofilecategory, Projectdefaultprofile


variable1Choices = (
        ('TCR','TCR'),
        ('SCR','SCR'),
        ('RQD','RQD'),
        ('N SPT','N SPT'),
        ('CL','CL'),
        ('PH','PH'),
        ('SC','SC'),
        ('LL','LL'),
        ('PL','PL'),
        ('PI','PI'),
        ('Moisture Content','Moisture Content'),
        ('Specific Gravity','Specific Gravity'),
        ('Bulk Density','Bulk Density'),
        ('Max Dry Density','Max Dry Density'),
        ('Min Dry Density','Min Dry Density'),
        ('Water Content','Water Content'),
        ('UCS','UCS'),
        ('Peak Angle of Friction','Peak Angle of Friction'),
        ('Residual Angle of Friction','Residual Angle of Friction'),
        ('Peak Cohesion','Peak Cohesion'),
        ('Residual Cohesion','Residual Cohesion'),
        ('Particle Size','Particle Size'),
        ('% passing 0.425mm','% passing 0.425mm'),
        ('% of Gravel','% of Gravel'),
        ('Water Level','Water Level')
    )

variable2Choices = (
        ('Elevation','Elevation'),
        ('Depth','Depth'),
        # ('Percentage Passing (%)','Percentage Passing (%)'),
    )

variable3Choices = (
        ('borehole','By Bore Hole'),
        ('machine','By Machine Type'),
        ('boreholeandmachine','By Bore Hole and Machine Type'),
        # ('boreholenumber','By Bore Number'),
    )

chartindexChoices = (
        ('First','First'),
        ('Second','Second'),
        ('Third','Third'),
        ('Fourth','Fourth'),
        ('Five','Five'),
        ('Six','Six'),
        ('Seven','Seven'),
        ('Eight','Eight'),
        ('Nine','Nine'),
        ('Ten','Ten'),
        ('Eleven','Eleven'),
        ('Twelveve','Twelveve'),
    )

class ProjectForm(forms.ModelForm):
    """form for project"""

    def clean_project_image(self):
        """image upload size"""
        photo = self.cleaned_data["thumnail"]
        if photo and photo.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                _("Please keep photo filesize under %s. filesize is slightly over %s") %
                                        (filesizeformat(settings.MAX_UPLOAD_SIZE),
                                         filesizeformat(photo.size)))
        return photo

    class Meta:
        """Meta"""
        model = ProjectTable
        fields = ("name", "summery", "location",
                  "number_of_bore_home","max_depth","thumnail")
        labels = {"name": "Project Name",
                  "summery": "Project Descriptions",
                  "thumnail": "Project Photo",
                  "location": "Project Location",
                  "number_of_bore_home": "Number of Bore Hole",
                  "max_depth": "Max Depth"
                  }

class ProjectAGSForm(forms.ModelForm):
    """form for project"""

    class Meta:
        """Meta"""
        model = ProjectAGS
        fields = ("ags_file",)
        labels = {
                  "ags_file": "Project AGS files"
                  }

class ContactForm(forms.ModelForm):
    """form for contact"""

    class Meta:
        """Meta"""
        model = ContactTable
        fields = ("name","email","phone","message")
        labels = {
                  "name": "Name",
                  "email": "Email",
                  "phone": "Phone",
                  "message": "Message",
                  }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'message': forms.TextInput(attrs={'placeholder': 'Message'})
        }
        

class ProfileForm(forms.ModelForm):
    """form for contact"""

    class Meta:
        """Meta"""
        model = Projectprofile
        fields = ("name","group","chart")
        labels = {
                  "name": "Name",
                  "group": "Group",
                  "chart": "Charts"
                  }

class ProfileDefaultCategoryForm(forms.ModelForm):
    """form for Default category"""

    class Meta:
        """Meta"""
        model = Projectdefaultprofilecategory
        fields = ("name",)
        labels = {
                  "name": "Name"
                  }

class ProfileDefaultForm(forms.ModelForm):
    """form for Default Profile"""
    variable1 = forms.ChoiceField(choices = variable1Choices)
    variable2 = forms.ChoiceField(choices = variable2Choices)
    variable3 = forms.ChoiceField(choices = variable3Choices)

    class Meta:
        """Meta"""
        model = Projectdefaultprofile
        fields = ("category","variable1","variable2","variable3",)
        labels = {
                  "category": "Category",
                  "variable1": "Variable One",
                  "variable2": "Variable Two",
                  "variable3": "Variable Three",
                  }
