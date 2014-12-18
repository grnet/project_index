# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Note'
        db.create_table('notes_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('notes', ['Note'])

        # Adding M2M table for field tag on 'Note'
        m2m_table_name = db.shorten_name('notes_note_tag')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('note', models.ForeignKey(orm['notes.note'], null=False)),
            ('tag', models.ForeignKey(orm['index.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['note_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Note'
        db.delete_table('notes_note')

        # Removing M2M table for field tag on 'Note'
        db.delete_table(db.shorten_name('notes_note_tag'))


    models = {
        'index.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'notes.note': {
            'Meta': {'object_name': 'Note'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['index.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['notes']