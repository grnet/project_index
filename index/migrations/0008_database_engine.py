# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_virtualenv_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='engine',
            field=models.CharField(default=b'mysql', max_length=255),
            preserve_default=True,
        ),
    ]
