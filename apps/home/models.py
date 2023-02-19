"""Models for project"""

import os
from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator


# Create your models here.
class ProjectTable(models.Model):
    """Module for project"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.DO_NOTHING)
    summery = models.CharField(max_length=500, null=True)
    thumnail = models.ImageField(upload_to ='project/thumnails/', blank=True, null=True)
    number_of_bore_home = models.CharField(max_length=20,blank=True,  null=True)
    max_depth = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=ProjectTable)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.thumnail.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=ProjectTable)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).thumnail.path
        try:
            new_img = instance.thumnail.path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass

class ProjectAGS(models.Model):
    """Module for project AGS"""
    project = models.ForeignKey(ProjectTable, on_delete = models.CASCADE, null=True)
    ags_file = models.FileField(upload_to='project/ags/',  validators=[FileExtensionValidator(allowed_extensions=["ags"])], blank=True, null=True)
    is_verified = models.BooleanField(default=False)

@receiver(post_delete, sender=ProjectAGS)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.ags_file.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=ProjectAGS)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).ags_file.path
        try:
            new_img = instance.ags_file.path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass

class ContactTable(models.Model):
    """Module for project"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15, null=True)
    message = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Projectprofile(models.Model):
    "project profile"
    project = models.ForeignKey(ProjectTable, on_delete = models.CASCADE, null=True)
    group = models.ForeignKey(Group,on_delete = models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    chart = JSONField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Projectdefaultprofilecategory(models.Model):
    "project profile"
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Projectdefaultprofile(models.Model):
    "project profile"
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Projectdefaultprofilecategory, on_delete = models.CASCADE, null=True)
    variable1 = models.CharField(max_length=200)
    variable2 = models.CharField(max_length=200)
    variable3 = models.CharField(max_length=200)
