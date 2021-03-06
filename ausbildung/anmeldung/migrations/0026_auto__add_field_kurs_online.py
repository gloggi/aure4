# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Kurs.online'
        db.add_column('anmeldung_kurs', 'online',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Kurs.online'
        db.delete_column('anmeldung_kurs', 'online')


    models = {
        'anmeldung.abteilung': {
            'Meta': {'object_name': 'Abteilung'},
            'abteilungsleitung': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'abteilungen'", 'symmetrical': 'False', 'through': "orm['anmeldung.Abteilungsleitung']", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'region': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'verband': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'default': "'ZH'", 'max_length': '100'})
        },
        'anmeldung.abteilungsleitung': {
            'Meta': {'object_name': 'Abteilungsleitung'},
            'abteilung': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leiter'", 'to': "orm['anmeldung.Abteilung']"}),
            'bis': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seit': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'al'", 'to': "orm['auth.User']"})
        },
        'anmeldung.alfeedback': {
            'Meta': {'object_name': 'ALFeedback'},
            'aktualisiert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'anmeldung': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['anmeldung.Anmeldung']", 'unique': 'True'}),
            'erstellt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kontaktperson': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mitteilung': ('django.db.models.fields.TextField', [], {}),
            'mobiltelefon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ok': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'anmeldung.anmeldung': {
            'Meta': {'unique_together': "(('kurs', 'user'),)", 'object_name': 'Anmeldung'},
            'abteilung': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anmeldung.Abteilung']"}),
            'ahv': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'aktualisiert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'anmeldung_erhalten': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'bahnabo': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'default': "'Keines'", 'max_length': '100'}),
            'bestaetigung': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bezahlt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'einheit': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'erstellt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'erstsprache': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'default': "''", 'max_length': '100'}),
            'foto': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'geburtsdatum': ('django.db.models.fields.DateField', [], {}),
            'geschlecht': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'js': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kurs': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'anmeldungen'", 'to': "orm['anmeldung.Kurs']"}),
            'land': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'default': "'CH'", 'max_length': '100'}),
            'mobiltelefon': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nachname': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'nationalitaet': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'default': "'CH'", 'max_length': '100'}),
            'notfallblatt_erhalten': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ort': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'pfadiname': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'plz': ('django.db.models.fields.IntegerField', [], {}),
            'schweinefleisch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'strasse': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'stufe': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'telefon': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'anmeldungen'", 'to': "orm['auth.User']"}),
            'vegetarier': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vorname': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'zusatz': ('ausbildung.anmeldung.fields.JSONField', [], {'null': 'True', 'blank': 'True'})
        },
        'anmeldung.kurs': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Kurs'},
            'aktualisiert': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'anmeldeschluss': ('django.db.models.fields.DateField', [], {}),
            'bis': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'erfasst': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hauptleiter': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jahrgang': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kursplaetze': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'nummer': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'teilnehmer': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'angemeldete_kurse'", 'symmetrical': 'False', 'through': "orm['anmeldung.Anmeldung']", 'to': "orm['auth.User']"}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'von': ('django.db.models.fields.DateField', [], {})
        },
        'anmeldung.notfallblatt': {
            'Meta': {'object_name': 'Notfallblatt'},
            'anmeldung': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['anmeldung.Anmeldung']", 'unique': 'True'}),
            'arzt_name': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'arzt_ort': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'arzt_plz': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'arzt_strasse': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'arzt_telefon': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gesundheitszustand': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kontakt': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'krankenkasse': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'land': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'medikamente': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'medis_ll': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobiltelefon': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ort': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'plz': ('django.db.models.fields.IntegerField', [], {}),
            'rega': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'starrkrampf': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'strasse': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'telefon': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'unfallversicherung': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'weiteres': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'anmeldung.zusatzfeld': {
            'Meta': {'object_name': 'Zusatzfeld'},
            'help_text': ('ausbildung.anmeldung.fields.OptionalCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kurs': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'zusatzfelder'", 'to': "orm['anmeldung.Kurs']"}),
            'label': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'typ': ('ausbildung.anmeldung.fields.RequiredCharField', [], {'max_length': '100'})
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

    complete_apps = ['anmeldung']