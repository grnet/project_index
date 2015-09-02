# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_remove_database_port'),
    ]

    operations = [
        migrations.RenameField(
            model_name='database',
            old_name='port_new',
            new_name='port',
        ),
    ]
