# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_auto_20151214_0756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='database',
        ),
        migrations.RemoveField(
            model_name='note',
            name='project',
        ),
    ]
