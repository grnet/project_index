# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Meeting'
        db.create_table('meetings_meeting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('outcome', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('meetings', ['Meeting'])


    def backwards(self, orm):
        # Deleting model 'Meeting'
        db.delete_table('meetings_meeting')


    models = {
        'meetings.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['meetings']