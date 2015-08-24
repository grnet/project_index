# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=255, blank=True)),
                ('passwd', models.CharField(max_length=255, blank=True)),
                ('host', models.CharField(max_length=255, blank=True)),
                ('port', models.IntegerField(max_length=255, blank=True)),
                ('app_name', models.CharField(max_length=255, blank=True)),
                ('instance', models.ForeignKey(to='index.Instance')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='model',
            name='instance',
        ),
        migrations.DeleteModel(
            name='Model',
        ),
    ]
