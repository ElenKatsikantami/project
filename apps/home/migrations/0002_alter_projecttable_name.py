# Generated by Django 3.2.6 on 2022-11-15 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttable',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
