# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Host'
        db.create_table('index_host', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('index', ['Host'])

        # Adding field 'Instance.host'
        db.add_column('index_instance', 'host',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['index.Host'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Host'
        db.delete_table('index_host')

        # Deleting field 'Instance.host'
        db.delete_column('index_instance', 'host_id')


    models = {
        'index.docs': {
            'Meta': {'object_name': 'Docs'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['index.Project']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'index.host': {
            'Meta': {'object_name': 'Host'},
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
            'Meta': {'object_name': 'Project'},
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
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'index.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['index']