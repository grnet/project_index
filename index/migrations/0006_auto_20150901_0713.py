# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_project_related_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='passwd',
            field=models.CharField(max_length=255, verbose_name=b'Password', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=255, verbose_name=b'Project'),
        ),
    ]
