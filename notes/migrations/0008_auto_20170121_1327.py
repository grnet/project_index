# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_auto_20151214_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='database',
            field=models.ManyToManyField(to='index.Database', blank=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='project',
            field=models.ManyToManyField(to='index.Project', blank=True),
        ),
    ]
