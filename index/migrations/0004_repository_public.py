# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_auto_20150824_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='public',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
