# Generated by Django 3.2.6 on 2023-03-06 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_merge_20230304_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectprofile',
            name='type',
            field=models.CharField(default='Default', max_length=7),
        ),
    ]
