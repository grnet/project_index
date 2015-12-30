# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0015_remove_database_instance'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_view', models.TextField(null=True, blank=True)),
                ('in_db', models.ForeignKey(related_name=b'in_db', blank=True, to='index.Database', null=True)),
                ('to_db', models.ForeignKey(related_name=b'to_db', blank=True, to='index.Database', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
