# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_auto_20151214_0822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='database_m2m',
            new_name='database',
        ),
        migrations.RenameField(
            model_name='note',
            old_name='project_m2m',
            new_name='project',
        ),
    ]
