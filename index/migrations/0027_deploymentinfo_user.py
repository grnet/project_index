# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0026_remove_repository_internal_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploymentinfo',
            name='user',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
