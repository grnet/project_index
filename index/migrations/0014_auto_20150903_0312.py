# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def combine_names(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Database = apps.get_model("index", "Database")
    for db in Database.objects.all():
        db.instances.add(db.instance)
        db.save()


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0013_database_instances'),
    ]

    operations = [
        migrations.RunPython(combine_names),
    ]
