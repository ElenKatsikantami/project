# Generated by Django 3.2.6 on 2023-02-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_projectexcel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectags',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='projectexcel',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
