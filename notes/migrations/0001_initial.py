# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('project', models.ForeignKey(to='index.Project')),
                ('tag', models.ManyToManyField(to='index.Tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
