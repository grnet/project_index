# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards_func(apps, schema_editor):
    notes = apps.get_model('notes', 'Note')
    for note in notes.objects.all():
        if note.project:
            note.project_m2m.add(note.project)
        if note.database:
            note.database_m2m.add(note.database)
        note.save()


def reverse_func(apps, schema_editor):
    notes = apps.get_model('notes', 'Note')
    for note in notes.objects.all():
        if note.project:
            try:
                note.project = note.project_m2m.all()[0]
            except IndexError:
                pass
        if note.database:
            try:
                note.database = note.database.all()[0]
            except IndexError:
                pass
        note.save()


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_auto_20151214_0805'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func, reverse_func
        ),
    ]
