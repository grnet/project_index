# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dependency'
        db.create_table('index_dependency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('package_name', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True)),
            ('pip_package_name', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal('index', ['Dependency'])

        # Adding M2M table for field dependencies on 'Project'
        m2m_table_name = db.shorten_name('index_project_dependencies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['index.project'], null=False)),
            ('dependency', models.ForeignKey(orm['index.dependency'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'dependency_id'])


    def backwards(self, orm):
        # Deleting model 'Dependency'
        db.delete_table('index_dependency')

        # Removing M2M table for field dependencies on 'Project'
        db.delete_table(db.shorten_name('index_project_dependencies'))


    models = {
        'index.dependency': {
            'Meta': {'object_name': 'Dependency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'package_name': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True'}),
            'pip_package_name': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
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
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'index.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['index.Dependency']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['index']