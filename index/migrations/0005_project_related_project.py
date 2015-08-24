# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_repository_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='related_project',
            field=models.ForeignKey(blank=True, to='index.Project', null=True),
            preserve_default=True,
        ),
    ]
