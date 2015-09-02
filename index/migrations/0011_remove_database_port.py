# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_auto_20150902_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='database',
            name='port',
        ),
    ]
