# Generated by Django 3.2.6 on 2023-03-11 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_auto_20230309_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectags',
            name='FractionAngle_activated',
            field=models.BooleanField(default=False),
        ),
    ]