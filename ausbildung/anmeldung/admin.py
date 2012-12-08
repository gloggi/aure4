# encoding: utf-8
from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

import reversion

from .models import Kurs, Zusatzfeld, Abteilung, Anmeldung, Notfallblatt


class ZusatzfeldInline(admin.TabularInline):
    model = Zusatzfeld
    extra = 0


class KursAdmin(reversion.VersionAdmin):
    list_display = ('name', 'nummer', 'anmeldeschluss', 'von', 'bis')
    search_fields = ('name', 'nummer', 'hauptleiter')
    inlines = [ZusatzfeldInline]
    prepopulated_fields = {'url': ('name',)}
    #date_hierarchy = 'von'


class AbteilungAdmin(reversion.VersionAdmin):
    list_display = ('name', 'region', 'verband')
    search_fields = ('name', 'region')


class NotfallblattInline(admin.StackedInline):
    model = Notfallblatt
    extra = 0
    fieldsets = (
        ('Kontakperson während dem Lager', {
            'fields': (
                'kontakt',
                ('strasse', 'plz', 'ort', 'land'),
                ('email', 'telefon', 'mobiltelefon')
            )
        }),
        ('Versicherung', {
            'fields': (('krankenkasse', 'unfallversicherung', 'rega'),)
        }),
        ('Hausarzt', {
            'fields': (
                ('arzt_name', 'arzt_telefon'),
                ('arzt_strasse', 'arzt_plz', 'arzt_ort'),
            )
        }),
        ('Gesundheitszustand', {
            'classes': ('collapse',),
            'fields': (
                'starrkrampf',
                'medikamente',
                'medis_ll',
                'gesundheitszustand',
                'weiteres',
            )
        })
    )


class AnmeldungAdmin(AdminImageMixin, reversion.VersionAdmin):
    list_display = ('__unicode__', 'kurs', 'abteilung', 'einheit')
    list_filter = ('kurs',)
    raw_id_fields = ('kurs',)
    inlines = (NotfallblattInline,)
    readonly_fields = ['erstellt', 'aktualisiert']
    fieldsets = [
        ('Admin', {
            'fields': (
                ('kurs', 'erstellt', 'aktualisiert'),
                ('anmeldung_erhalten', 'notfallblatt_erhalten', 'bezahlt'),
            )
        }),
        ('Personalien', {
            'fields': (
                'foto',
                ('pfadiname', 'strasse', 'email'),
                ('vorname', 'plz', 'telefon'),
                ('nachname', 'ort', 'mobiltelefon'),
                ('geburtsdatum', 'geschlecht'),
            )
        }),
        ('Pfadizugehörigkeit', {
            'fields': (('abteilung', 'einheit', 'stufe'),)
        }),
        ('Weitere Daten', {
            'fields': (
                ('bahnabo', 'nationalitaet', 'land', 'erstsprache'),
                ('vegetarier', 'schweinefleisch', 'bestaetigung'),
            )
        }),
        ('Zusatzdaten', {
            'classes': ('collapse',),
            'fields': ('zusatz',)
        })
    ]

    class Media:
        css = {
            "all": ("css/admin.css",)
        }


admin.site.register(Abteilung, AbteilungAdmin)
admin.site.register(Kurs, KursAdmin)
admin.site.register(Anmeldung, AnmeldungAdmin)
