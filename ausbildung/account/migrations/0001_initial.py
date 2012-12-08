# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profil'
        db.create_table('account_profil', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('erstellt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('aktualisiert', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('pfadiname', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('geschlecht', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('geburtsdatum', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('foto', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('strasse', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('plz', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ort', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('land', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(default='CH', max_length=100, null=True, blank=True)),
            ('telefon', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('mobiltelefon', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('abteilung', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anmeldung.Abteilung'], null=True, blank=True)),
            ('einheit', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('stufe', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(max_length=100, null=True, blank=True)),
            ('nationalitaet', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(default='CH', max_length=100, null=True, blank=True)),
            ('erstsprache', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(default='', max_length=100, null=True, blank=True)),
            ('bahnabo', self.gf('ausbildung.anmeldung.fields.OptionalCharField')(default='Keines', max_length=100, null=True, blank=True)),
            ('vegetarier', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('schweinefleisch', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('account', ['Profil'])


    def backwards(self, orm):
        # Deleting model 'Profil'
        db.delete_table('account_profil')


    models = {
        'account.profil': {
            'Meta': {'object_name': 'Profil'},
            'abteilung': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anmeldung.Abteilung']", 'null': 'True', 'blank': 'True'}),
            'aktualisiert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'bahnabo': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'default': "'Keines'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'einheit': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'erstellt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'erstsprache': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'foto': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'geburtsdatum': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'geschlecht': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'default': "'CH'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mobiltelefon': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nationalitaet': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'default': "'CH'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ort': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pfadiname': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'plz': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'schweinefleisch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'strasse': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'stufe': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'telefon': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'vegetarier': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'anmeldung.abteilung': {
            'Meta': {'object_name': 'Abteilung'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'region': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'verband': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'default': "'ZH'", 'max_length': '100'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['account']