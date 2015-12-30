# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0016_viewdependency'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewdependency',
            name='name',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
