# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_note_database'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='database',
            field=models.ForeignKey(blank=True, to='index.Database', null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='project',
            field=models.ForeignKey(blank=True, to='index.Project', null=True),
        ),
    ]
