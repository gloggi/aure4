# encoding: utf-8
import csv

from datetime import date

from django.contrib import admin
from django.contrib.admin.util import lookup_field
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_unicode
from django.utils.timezone import now

from sorl.thumbnail.admin import AdminImageMixin

import reversion

from .models import (Kurs, Zusatzfeld, Abteilung, Abteilungsleitung, Anmeldung,
    Notfallblatt, ALFeedback)


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
    fieldsets = [
        ('Feedback', {'fields': ('ok', 'user', 'mitteilung')}),
        ('Kontaktperson', {'fields': (('kontaktperson', 'mobiltelefon'),)})
    ]


def sportdb_export(modeladmin, request, queryset):
    response = HttpResponse(mimetype='text/csv')
    timestamp = now().strftime('%d%m%y_%H%M')
    filename = 'sportdb_export_%s.csv' % timestamp
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = csv.writer(response, delimiter=';')

    header = (
        'NDBJS_PERS_NR',
        'GESCHLECHT',
        'NAME',
        'VORNAME',
        'GEB_DATUM',
        'STRASSE',
        'PLZ',
        'ORT',
        'LAND',
        'NATIONALITAET',
        'ERSTSPRACHE',
        'KLASSE/GRUPPE'
    )

    writer.writerow([row for row in header])

    fields = (
        'js',
        'geschlecht',
        'nachname',
        'vorname',
        'geburtsdatum',
        'strasse',
        'plz',
        'ort',
        'land',
        'nationalitaet',
        'erstsprache',
    )

    def serialize(obj, field):
        f, attr, value = lookup_field(field, obj, modeladmin)
        value = value if value is not None else ''
        if type(value) == date:
            value = value.strftime('%d.%m.%Y')
        return force_unicode(value).encode('utf-8')

    for obj in queryset:
        writer.writerow([serialize(obj, field) for field in fields] + [''])

    return response

sportdb_export.short_description = 'Sportdb Export (CSV, UTF-8)'


def print_export(modeladmin, request, queryset):
    return render(request, 'anmeldung/anmeldung_print.html', {
        'anmeldungen': queryset
    })
print_export.short_description = 'Anmeldungen Drucken'


def notfallblatt_export(modeladmin, request, queryset):
    return render(request, 'anmeldung/notfallblatt_print.html', {
        'anmeldungen': queryset
    })
notfallblatt_export.short_description = 'Notfallblätter Drucken'


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
        ('alfeedback__ok', admin.BooleanFieldListFilter),
        ('notfallblatt_erhalten', admin.BooleanFieldListFilter),
        ('anmeldung_erhalten', admin.BooleanFieldListFilter),
        ('bezahlt', admin.BooleanFieldListFilter),
    )
    list_search = ('pfadiname', 'vorname', 'nachname', 'email')
    actions = [sportdb_export, print_export, notfallblatt_export]
    raw_id_fields = ('user', 'kurs',)
    inlines = (NotfallblattInline, ALFeedbackInline)
    readonly_fields = ['erstellt', 'aktualisiert']
    fieldsets = [
        ('Admin', {
            'fields': (
                ('user', 'kurs', 'erstellt', 'aktualisiert'),
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
                ('js', 'ahv'),
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

    def geschlecht_kurz(self, obj):
        return 'm' if obj.geschlecht else 'w'
    geschlecht_kurz.short_description = 'Geschl.'

    def pfadi(self, obj):
        return u'%s / %s' % (obj.abteilung.name, obj.einheit)

    def al_ok(self, obj):
        try:
            return obj.alfeedback.ok
        except:
            return None
    al_ok.short_description = 'AL OK'
    al_ok.boolean = True

    def nfb(self, obj):
        try:
            obj.notfallblatt
            return True
        except:
            return obj.notfallblatt_erhalten is not None
    nfb.short_description = 'NFB'
    nfb.boolean = True

    def anmeldung_seki(self, obj):
        return obj.anmeldung_erhalten is not None
    anmeldung_seki.short_description = 'Anm.'
    anmeldung_seki.boolean = True

    def zahlung(self, obj):
        return obj.bezahlt is not None
    zahlung.boolean = True


admin.site.register(Abteilung, AbteilungAdmin)
admin.site.register(Kurs, KursAdmin)
admin.site.register(Anmeldung, AnmeldungAdmin)

from report_builder.models import Report
from report_builder.admin import ReportAdmin

admin.site.unregister(Report)


class SaveAsReportAdmin(ReportAdmin):
    save_as = True

admin.site.register(Report, SaveAsReportAdmin)
