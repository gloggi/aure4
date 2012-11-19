
from django.contrib import admin

from .models import Kurs, Abteilung, Anmeldung


class KursAdmin(admin.ModelAdmin):
    list_display = ('name', 'nummer', 'anmeldeschluss', 'von', 'bis')
    search_fields = ('name', 'nummer', 'hauptleiter')
    prepopulated_fields = {'url': ('name',)}
    #date_hierarchy = 'von'


class AbteilungAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'verband')
    search_fields = ('name', 'region')


class AnmeldungAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'kurs', 'abteilung', 'einheit')
    list_filter = ('kurs',)
    radio_fields = {
        'geschlecht': admin.HORIZONTAL,
        'bahnabo': admin.HORIZONTAL,
        'stufe': admin.VERTICAL
    }
    raw_id_fields = ('kurs',)


admin.site.register(Abteilung, AbteilungAdmin)
admin.site.register(Kurs, KursAdmin)
admin.site.register(Anmeldung, AnmeldungAdmin)
