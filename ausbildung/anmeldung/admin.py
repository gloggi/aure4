# encoding: utf-8


from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Kurs, Abteilung, Anmeldung


class KursAdmin(admin.ModelAdmin):
    list_display = ('name', 'nummer', 'anmeldeschluss', 'von', 'bis')
    search_fields = ('name', 'nummer', 'hauptleiter')
    prepopulated_fields = {'url': ('name',)}
    #date_hierarchy = 'von'


class AbteilungAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'verband')
    search_fields = ('name', 'region')


class AnmeldungAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('__unicode__', 'kurs', 'abteilung', 'einheit')
    list_filter = ('kurs',)
    raw_id_fields = ('kurs',)
    fieldsets = (
        ('Admin', {
            'fields': (('seki', 'notfallblatt', 'bezahlt'),)
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
        ('Weiter Daten', {
            'fields': (
                ('bahnabo', 'nationalitaet', 'land', 'erstsprache'),
                ('vegetarier', 'schweinefleisch', 'bestaetigung'),
            )
        })
    )

    class Media:
        css = {
            "all": ("css/admin.css",)
        }


admin.site.register(Abteilung, AbteilungAdmin)
admin.site.register(Kurs, KursAdmin)
admin.site.register(Anmeldung, AnmeldungAdmin)
