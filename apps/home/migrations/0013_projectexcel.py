# Generated by Django 3.2.6 on 2023-02-25 11:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_projectprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectExcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(upload_to='project/excel/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx'])])),
                ('is_verified', models.BooleanField(default=False)),
                ('ags_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.projectags')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.projecttable')),
            ],
        ),
    ]
