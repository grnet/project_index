# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0019_auto_20151230_0329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viewdependency',
            name='to_db',
        ),
    ]
