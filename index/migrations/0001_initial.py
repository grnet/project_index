# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cronjob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('command', models.CharField(max_length=255)),
                ('period', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('package_name', models.SlugField(max_length=255, null=True, blank=True)),
                ('pip_package_name', models.SlugField(max_length=255)),
                ('version', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Docs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instance_type', models.CharField(max_length=3, choices=[('pro', 'Production'), ('stg', 'Staging'), ('dev', 'Development')])),
                ('url', models.URLField(blank=True)),
                ('path', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('host', models.ForeignKey(blank=True, to='index.Host', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('description', models.TextField(help_text='Auto generated if blank and repo is public', null=True, blank=True)),
                ('dependency_file', models.FileField(null=True, upload_to=b'dependencies', blank=True)),
                ('public', models.BooleanField(default=True)),
                ('dependencies', models.ManyToManyField(to='index.Dependency', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(null=True, blank=True)),
                ('project', models.ForeignKey(to='index.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Virtualenv',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='tag',
            field=models.ManyToManyField(to='index.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instance',
            name='project',
            field=models.ForeignKey(to='index.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instance',
            name='virtualenv',
            field=models.ForeignKey(blank=True, to='index.Virtualenv', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='docs',
            name='project',
            field=models.ForeignKey(to='index.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cronjob',
            name='hosts',
            field=models.ManyToManyField(to='index.Host'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cronjob',
            name='project',
            field=models.ForeignKey(blank=True, to='index.Project', null=True),
            preserve_default=True,
        ),
    ]
