from django.conf.urls import patterns, url

urlpatterns = patterns('ausbildung.anmeldung.views',
    url(r'^$', 'kurse',
        name='anmeldung_kurse'),

    url(r'^(?P<kurs>[-\w]+)/$', 'anmeldung_form',
        name='anmeldung_form'),
    url(r'^(?P<kurs>[-\w]+)/view/$', 'anmeldung_view',
        name='anmeldung_view'),
    url(r'^(?P<kurs>[-\w]+)/edit/$', 'anmeldung_edit',
        name='anmeldung_edit'),
    url(r'^(?P<kurs>[-\w]+)/print/$', 'anmeldung_print',
        name='anmeldung_print'),
    url(r'^(?P<kurs>[-\w]+)/notfallblatt/$', 'notfallblatt_form',
        name='notfallblatt_form'),
    url(r'^(?P<kurs>[-\w]+)/notfallblatt/edit/$', 'notfallblatt_edit',
        name='notfallblatt_edit'),
)
