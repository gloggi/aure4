# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Kurs'
        db.create_table('anmeldung_kurs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('nummer', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('von', self.gf('django.db.models.fields.DateField')()),
            ('bis', self.gf('django.db.models.fields.DateField')()),
            ('anmeldeschluss', self.gf('django.db.models.fields.DateField')()),
            ('hauptleiter', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('erfasst', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('aktualisiert', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('anmeldung', ['Kurs'])

        # Adding model 'Abteilung'
        db.create_table('anmeldung_abteilung', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(max_length=100)),
            ('region', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('verband', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(default='ZH', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('anmeldung', ['Abteilung'])

        # Adding model 'Anmeldung'
        db.create_table('anmeldung_anmeldung', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kurs', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anmeldung.Kurs'])),
            ('geschlecht', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(max_length=100)),
            ('pfadiname', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(max_length=100)),
            ('vorname', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(max_length=100)),
            ('nachname', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(max_length=100)),
            ('geburtsdatum', self.gf('django.db.models.fields.DateField')()),
            ('strasse', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(max_length=100)),
            ('plz', self.gf('django.db.models.fields.IntegerField')()),
            ('ort', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(max_length=100)),
            ('land', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(default='CH', max_length=100)),
            ('nationalitaet', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(default='CH', max_length=100)),
            ('erstsprache', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(default='', max_length=100)),
            ('bahnabo', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(default='Keines', max_length=100)),
            ('abteilung', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anmeldung.Abteilung'])),
            ('einheit', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(max_length=100)),
            ('stufe', self.gf('ausbildung.anmeldung.fields.RequiredCharField')(max_length=100)),
            ('js', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ahv', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('telefon', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('mobiltelefon', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('vegetarier', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('schweinefleisch', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bestaetigung', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('anmeldung', ['Anmeldung'])


    def backwards(self, orm):
        # Deleting model 'Kurs'
        db.delete_table('anmeldung_kurs')

        # Deleting model 'Abteilung'
        db.delete_table('anmeldung_abteilung')

        # Deleting model 'Anmeldung'
        db.delete_table('anmeldung_anmeldung')


    models = {
        'anmeldung.abteilung': {
            'Meta': {'object_name': 'Abteilung'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'region': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'verband': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'default': "'ZH'", 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'anmeldung.anmeldung': {
            'Meta': {'object_name': 'Anmeldung'},
            'abteilung': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anmeldung.Abteilung']"}),
            'ahv': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bahnabo': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'default': "'Keines'", 'max_length': '100'}),
            'bestaetigung': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'einheit': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'erstsprache': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'default': "''", 'max_length': '100'}),
            'geburtsdatum': ('django.db.models.fields.DateField', [], {}),
            'geschlecht': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'js': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kurs': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anmeldung.Kurs']"}),
            'land': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'default': "'CH'", 'max_length': '100'}),
            'mobiltelefon': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nachname': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'nationalitaet': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'default': "'CH'", 'max_length': '100'}),
            'ort': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'pfadiname': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'plz': ('django.db.models.fields.IntegerField', [], {}),
            'schweinefleisch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'strasse': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'stufe': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'telefon': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vegetarier': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vorname': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'})
        },
        'anmeldung.kurs': {
            'Meta': {'object_name': 'Kurs'},
            'aktualisiert': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'anmeldeschluss': ('django.db.models.fields.DateField', [], {}),
            'bis': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'erfasst': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hauptleiter': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'nummer': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'von': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['anmeldung']