# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0015_remove_database_instance'),
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='database',
            field=models.ForeignKey(to='index.Database', null=True),
            preserve_default=True,
        ),
    ]
