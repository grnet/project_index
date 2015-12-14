# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0015_remove_database_instance'),
        ('notes', '0003_auto_20151201_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='database_m2m',
            field=models.ManyToManyField(to='index.Database', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='project_m2m',
            field=models.ManyToManyField(to='index.Project', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='note',
            name='database',
            field=models.ForeignKey(related_name=b'db_notes', blank=True, to='index.Database', null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='project',
            field=models.ForeignKey(related_name=b'project_notes', blank=True, to='index.Project', null=True),
        ),
    ]
