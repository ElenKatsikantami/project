# Generated by Django 3.2.6 on 2023-02-19 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_projectprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projectdefaultprofilecategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
