# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0022_viewdependency_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='instances',
            field=models.ManyToManyField(related_name='instance_info', to='index.Instance', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='dependencies',
            field=models.ManyToManyField(to='index.Dependency', blank=True),
        ),
        migrations.AlterField(
            model_name='viewdependency',
            name='to_dbs',
            field=models.ManyToManyField(related_name='to_dbs', to='index.Database', blank=True),
        ),
    ]
