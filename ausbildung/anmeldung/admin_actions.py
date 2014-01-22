# encoding: utf-8

import unicodecsv

from datetime import date

from django.contrib.admin.util import lookup_field
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_unicode
from django.utils.timezone import now

def csv_export(modeladmin, queryset, name, header, fields):
    response = HttpResponse(mimetype='text/csv')
    timestamp = now().strftime('%d%m%y_%H%M')
    filename = '%s_%s.csv' % (name, timestamp)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = unicodecsv.writer(response, delimiter=';')

    writer.writerow([row for row in header])

    def serialize(obj, field):
        f, attr, value = lookup_field(field, obj, modeladmin)
        value = value if value is not None else ''
        if type(value) == date:
            value = value.strftime('%d.%m.%Y')
        if type(value) == bool:
            value = 1 if value else 0
        return force_unicode(value).encode('utf-8')

    for obj in queryset:
        writer.writerow([serialize(obj, field) for field in fields] + [''])

    return response

def sportdb_export(modeladmin, request, queryset):
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

    return csv_export(modeladmin, queryset, 'sportdb', header, fields)
sportdb_export.short_description = 'Sportdb exportieren (CSV, UTF-8)'


def list_export(modeladmin, request, queryset):
    fields = (
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
        'geschlecht',
        'abteilung',
        'einheit',
        'anmeldung_erhalten',
        'notfallblatt_erhalten',
        'bezahlt',
    )
    header = [f.upper() for f in fields]
    return csv_export(modeladmin, queryset, 'tn', header, fields)
list_export.short_description = 'TN-Liste exportieren'

def print_export(modeladmin, request, queryset):
    return render(request, 'anmeldung/anmeldung_print.html', {
        'anmeldungen': queryset
    })
print_export.short_description = 'Anmeldungen Drucken'

def print_confirmation(modeladmin, request, queryset):
    return render(request, 'anmeldung/confirm_print.html', {
        'anmeldungen': queryset
    })
print_confirmation.short_description = u'Bestätigung drucken'

def notfallblatt_export(modeladmin, request, queryset):
    return render(request, 'anmeldung/notfallblatt_print.html', {
        'anmeldungen': queryset
    })
notfallblatt_export.short_description = 'Notfallblätter Drucken'