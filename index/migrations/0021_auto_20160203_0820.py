# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0020_remove_viewdependency_to_db'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='instances',
            field=models.ManyToManyField(related_name=b'instance_info', null=True, to=b'index.Instance', blank=True),
        ),
    ]
