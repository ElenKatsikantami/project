# Generated by Django 3.2.6 on 2023-03-08 00:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_projectprofile_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectexcel',
            name='excel_file',
            field=models.FileField(blank=True, null=False, upload_to='project/excel/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx'])]),
        ),
    ]