from django.conf.urls import patterns, url

urlpatterns = patterns('ausbildung.anmeldung.views',
    url(r'^$', 'index',
        name='anmeldung_index'),

    url(r'kurse/', 'kurse_list',
        name='kurse_list'),

    url(r'^kurs/(?P<kurs>[-\w]+)/anmelden/$', 'anmeldung_form',
        name='anmeldung_form'),
    url(r'^kurs/(?P<kurs>[-\w]+)/anmeldung/$', 'anmeldung_view',
        name='anmeldung_view'),
    url(r'^kurs/(?P<kurs>[-\w]+)/anmeldung/edit/$', 'anmeldung_edit',
        name='anmeldung_edit'),
    url(r'^kurs/(?P<kurs>[-\w]+)/anmeldung/print/$', 'anmeldung_print',
        name='anmeldung_print'),
    url(r'^kurs/(?P<kurs>[-\w]+)/notfallblatt/$', 'notfallblatt_form',
        name='notfallblatt_form'),
    url(r'^kurs/(?P<kurs>[-\w]+)/notfallblatt/edit/$', 'notfallblatt_edit',
        name='notfallblatt_edit'),
)
