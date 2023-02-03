"""forms for home app"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.conf import settings
from .models import ProjectTable,ProjectAGS,ContactTable,Projectprofile


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
