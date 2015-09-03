# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0012_auto_20150902_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='instances',
            field=models.ManyToManyField(related_name=b'instance_info', to='index.Instance'),
            preserve_default=True,
        ),
    ]
