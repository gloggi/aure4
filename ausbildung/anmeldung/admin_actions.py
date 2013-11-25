# encoding: utf-8

import csv

from datetime import date

from django.contrib.admin.util import lookup_field
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_unicode
from django.utils.timezone import now


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