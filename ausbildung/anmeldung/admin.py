# encoding: utf-8

from django.contrib import admin
from django.db import models

from sorl.thumbnail.admin import AdminImageMixin

from suit.widgets import SuitSplitDateTimeWidget

import reversion

from .models import (Kurs, Zusatzfeld, Abteilung, Abteilungsleitung, Anmeldung,
    Notfallblatt, ALFeedback)

from .admin_actions import sportdb_export, print_export, notfallblatt_export


class ZusatzfeldInline(admin.TabularInline):
    model = Zusatzfeld
    extra = 0


class KursAdmin(reversion.VersionAdmin):
    list_display = ('name', 'nummer', 'anmeldeschluss', 'von', 'bis')
    search_fields = ('name', 'nummer', 'hauptleiter')
    inlines = [ZusatzfeldInline]
    prepopulated_fields = {'url': ('name',)}
    #date_hierarchy = 'von'


class AbteilungsleitungInline(admin.StackedInline):
    model = Abteilungsleitung
    extra = 0


class AbteilungAdmin(reversion.VersionAdmin):
    list_display = ('name', 'region', 'verband')
    search_fields = ('name', 'region')
    readonly_fields = ('slug',)
    inlines = (AbteilungsleitungInline,)


class NotfallblattInline(admin.StackedInline):
    model = Notfallblatt
    extra = 0
    suit_classes = 'suit-tab suit-tab-notfallblatt'
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


class ALFeedbackInline(admin.StackedInline):
    model = ALFeedback
    extra = 0
    raw_id_fields = ('user',)
    suit_classes = 'suit-tab suit-tab-alfeedback'
    fieldsets = [
        ('Feedback', {'fields': ('ok', 'user', 'mitteilung')}),
        ('Kontaktperson', {'fields': (('kontaktperson', 'mobiltelefon'),)})
    ]



class AnmeldungAdmin(AdminImageMixin, reversion.VersionAdmin):
    list_display = (
        'pfadiname',
        'vorname',
        'nachname',
        'strasse',
        'plz',
        'ort',
        'geburtsdatum',
        'email',
        'telefon',
        'mobiltelefon',
        'vegetarier',
        'geschlecht_kurz',
        'pfadi',
        'al_ok',
        'nfb',
        'anmeldung_seki',
        'zahlung',
    )
    list_display_links = (
        'pfadiname',
        'vorname',
        'nachname',
    )
    list_filter = (
        'kurs',
    )
    list_search = ('pfadiname', 'vorname', 'nachname', 'email')
    actions = [sportdb_export, print_export, notfallblatt_export]
    raw_id_fields = ('user', 'kurs',)
    inlines = (NotfallblattInline, ALFeedbackInline)
    readonly_fields = ['erstellt', 'aktualisiert']
    formfield_overrides = {
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
    }
    suit_form_tabs = (
        ('admin', 'Admin'),
        ('personalien', 'Personalien'),
        ('weitere', 'Weitere Daten'),
        ('alfeedback', 'AL Feedback'),
        ('notfallblatt', 'Notfallblatt'),
    )
    fieldsets = [
        ('Admin', {
            'classes': ('suit-tab suit-tab-admin',),
            'fields': (
                'user',
                'kurs',
                'erstellt',
                'aktualisiert',
                'anmeldung_erhalten',
                'notfallblatt_erhalten',
                'bezahlt',
            )
        }),
        ('Pfadizugehörigkeit', {
            'classes': ('suit-tab suit-tab-admin',),
            'fields': ('abteilung', 'einheit', 'stufe')
        }),
        ('Personalien', {
            'classes': ('suit-tab suit-tab-personalien',),
            'fields': (
                'foto',
                'pfadiname',
                'strasse',
                'email',
                'vorname',
                'plz',
                'telefon',
                'nachname',
                'ort',
                'mobiltelefon',
                'geburtsdatum',
                'geschlecht',
            )
        }),
        ('Weitere Daten', {
            'classes': ('suit-tab suit-tab-weitere',),
            'fields': (
                'bahnabo',
                'nationalitaet',
                'land',
                'erstsprache',
                'js',
                'ahv',
                'vegetarier',
                'schweinefleisch',
                'bestaetigung',
            )
        }),
        ('Zusatzdaten', {
            'classes': ('collapse suit-tab suit-tab-weitere',),
            'fields': ('zusatz',)
        }),
    ]

    def geschlecht_kurz(self, obj):
        return 'm' if obj.geschlecht == '1' else 'w'
    geschlecht_kurz.short_description = 'Geschl.'
    geschlecht_kurz.admin_order_field = 'geschlecht'

    def pfadi(self, obj):
        return u'%s / %s' % (obj.abteilung.name, obj.einheit)
    pfadi.admin_order_field = 'abteilung'

    def al_ok(self, obj):
        try:
            return obj.alfeedback.ok
        except:
            return None
    al_ok.short_description = 'AL OK'
    al_ok.admin_order_field = 'alfeedback__ok'
    al_ok.boolean = True

    def nfb(self, obj):
        return obj.notfallblatt_erhalten is not None
    nfb.short_description = 'NFB'
    nfb.admin_order_field='notfallblatt_erhalten'
    nfb.boolean = True

    def anmeldung_seki(self, obj):
        return obj.anmeldung_erhalten is not None
    anmeldung_seki.short_description = 'Anm.'
    anmeldung_seki.admin_order_field = 'anmeldung_erhalten'
    anmeldung_seki.boolean = True

    def zahlung(self, obj):
        return obj.bezahlt is not None
    zahlung.admin_order_field = 'anmeldung_erhalten'
    zahlung.boolean = True



admin.site.register(Abteilung, AbteilungAdmin)
admin.site.register(Kurs, KursAdmin)
admin.site.register(Anmeldung, AnmeldungAdmin)
