# Generated by Django 3.2.6 on 2022-12-08 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20221121_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=500, null=True)),
                ('message', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
