# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0023_auto_20170121_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeploymentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('commit_hash', models.CharField(max_length=256)),
                ('instance', models.ForeignKey(to='index.Instance')),
            ],
        ),
    ]
