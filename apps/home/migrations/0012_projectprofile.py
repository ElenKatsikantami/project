# Generated by Django 3.2.6 on 2023-01-23 17:25

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('home', '0011_alter_contacttable_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projectprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('chart', django.contrib.postgres.fields.jsonb.JSONField()),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.projecttable')),
            ],
        ),
    ]
