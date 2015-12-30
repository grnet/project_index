# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0017_viewdependency_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewdependency',
            name='to_dbs',
            field=models.ManyToManyField(related_name=b'to_dbs', null=True, to='index.Database', blank=True),
            preserve_default=True,
        ),
    ]
