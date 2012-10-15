
from django.contrib import admin

from .models import Kurs, Anmeldung

class KursAdmin(admin.ModelAdmin):
    list_display = ('name', 'nummer', 'von', 'bis', 'hauptleiter')
    search_fields = ('name', 'nummer', 'von', 'bis', 'hauptleiter')
    #date_hierarchy = 'von'

class AnmeldungAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'kurs', 'abteilung', 'einheit')
    list_filter = ('kurs',)
    radio_fields = {
        'geschlecht': admin.HORIZONTAL,
        'bahnabo': admin.HORIZONTAL,
        'stufe': admin.VERTICAL
    }
    raw_id_fields = ('kurs',)

admin.site.register(Kurs, KursAdmin)

admin.site.register(Anmeldung, AnmeldungAdmin)
