# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table('index_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dependency_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('index', ['Project'])

        # Adding M2M table for field tag on 'Project'
        m2m_table_name = db.shorten_name('index_project_tag')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['index.project'], null=False)),
            ('tag', models.ForeignKey(orm['index.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'tag_id'])

        # Adding M2M table for field dependencies on 'Project'
        m2m_table_name = db.shorten_name('index_project_dependencies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['index.project'], null=False)),
            ('dependency', models.ForeignKey(orm['index.dependency'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'dependency_id'])

        # Adding model 'Repository'
        db.create_table('index_repository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['index.Project'])),
        ))
        db.send_create_signal('index', ['Repository'])

        # Adding model 'Host'
        db.create_table('index_host', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('index', ['Host'])

        # Adding model 'Virtualenv'
        db.create_table('index_virtualenv', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('index', ['Virtualenv'])

        # Adding model 'Instance'
        db.create_table('index_instance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['index.Project'])),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['index.Host'], null=True, blank=True)),
            ('virtualenv', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['index.Virtualenv'], null=True, blank=True)),
        ))
        db.send_create_signal('index', ['Instance'])

        # Adding model 'Docs'
        db.create_table('index_docs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['index.Project'])),
        ))
        db.send_create_signal('index', ['Docs'])

        # Adding model 'Tag'
        db.create_table('index_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('index', ['Tag'])

        # Adding model 'Dependency'
        db.create_table('index_dependency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('package_name', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True)),
            ('pip_package_name', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('index', ['Dependency'])

        # Adding model 'Cronjob'
        db.create_table('index_cronjob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['index.Project'], null=True, blank=True)),
            ('command', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('period', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('index', ['Cronjob'])

        # Adding M2M table for field hosts on 'Cronjob'
        m2m_table_name = db.shorten_name('index_cronjob_hosts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cronjob', models.ForeignKey(orm['index.cronjob'], null=False)),
            ('host', models.ForeignKey(orm['index.host'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cronjob_id', 'host_id'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table('index_project')

        # Removing M2M table for field tag on 'Project'
        db.delete_table(db.shorten_name('index_project_tag'))

        # Removing M2M table for field dependencies on 'Project'
        db.delete_table(db.shorten_name('index_project_dependencies'))

        # Deleting model 'Repository'
        db.delete_table('index_repository')

        # Deleting model 'Host'
        db.delete_table('index_host')

        # Deleting model 'Virtualenv'
        db.delete_table('index_virtualenv')

        # Deleting model 'Instance'
        db.delete_table('index_instance')

        # Deleting model 'Docs'
        db.delete_table('index_docs')

        # Deleting model 'Tag'
        db.delete_table('index_tag')

        # Deleting model 'Dependency'
        db.delete_table('index_dependency')

        # Deleting model 'Cronjob'
        db.delete_table('index_cronjob')

        # Removing M2M table for field hosts on 'Cronjob'
        db.delete_table(db.shorten_name('index_cronjob_hosts'))


    models = {
        'index.cronjob': {
            'Meta': {'object_name': 'Cronjob'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hosts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['index.Host']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['index.Project']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'index.dependency': {
            'Meta': {'ordering': "['name']", 'object_name': 'Dependency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'package_name': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pip_package_name': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'index.docs': {
            'Meta': {'object_name': 'Docs'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['index.Project']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'index.host': {
            'Meta': {'ordering': "['name']", 'object_name': 'Host'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'index.instance': {
            'Meta': {'object_name': 'Instance'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['index.Host']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['index.Project']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'virtualenv': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['index.Virtualenv']", 'null': 'True', 'blank': 'True'})
        },
        'index.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['index.Dependency']", 'null': 'True', 'blank': 'True'}),
            'dependency_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['index.Tag']", 'symmetrical': 'False'})
        },
        'index.repository': {
            'Meta': {'object_name': 'Repository'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['index.Project']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'index.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'index.virtualenv': {
            'Meta': {'object_name': 'Virtualenv'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['index']