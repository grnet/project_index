# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def make_many_dependencies(apps, schema_editor):

    view_dependency = apps.get_model('index', 'ViewDependency')

    for dependency in view_dependency.objects.all():
        dependency.to_dbs.add(dependency.to_db)


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0018_viewdependency_to_dbs'),
    ]

    operations = [
        migrations.RunPython(make_many_dependencies),
    ]
