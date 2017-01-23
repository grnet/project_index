# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0024_deploymentinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='deployable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='repository',
            name='internal_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
