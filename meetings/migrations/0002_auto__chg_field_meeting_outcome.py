# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Meeting.outcome'
        db.alter_column('meetings_meeting', 'outcome', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Meeting.outcome'
        raise RuntimeError("Cannot reverse this migration. 'Meeting.outcome' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Meeting.outcome'
        db.alter_column('meetings_meeting', 'outcome', self.gf('django.db.models.fields.TextField')())

    models = {
        'meetings.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome': ('django.db.models.fields.TextField', [], {'null': 'True'})
        }
    }

    complete_apps = ['meetings']