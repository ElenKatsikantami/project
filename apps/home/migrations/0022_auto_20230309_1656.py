# Generated by Django 3.2.6 on 2023-03-09 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_alter_projectexcel_excel_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectags',
            name='nspt_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projectags',
            name='rdSkempton_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projectags',
            name='rdTerzaghi_activated',
            field=models.BooleanField(default=False),
        ),
    ]
