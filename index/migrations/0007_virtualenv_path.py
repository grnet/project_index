# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_auto_20150901_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualenv',
            name='path',
            field=models.CharField(default=b'Please enter a valid virtualenv path', max_length=255),
            preserve_default=True,
        ),
    ]
