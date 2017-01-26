# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0025_auto_20170123_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repository',
            name='internal_id',
        ),
    ]
