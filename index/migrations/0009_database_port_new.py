# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_database_engine'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='port_new',
            field=models.CharField(default=b'default', max_length=255),
            preserve_default=True,
        ),
    ]
