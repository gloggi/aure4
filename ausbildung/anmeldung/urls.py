from django.conf.urls import patterns, url

urlpatterns = patterns('ausbildung.anmeldung.views',
    url(r'^$', 'kurse',
        name='anmeldung_kurse'),
    url(r'^fertig/$', 'anmeldung_done',
        name='anmeldung_done'),
    url(r'^(?P<kurs>[-\w]+)/$', 'anmeldung',
        name='anmeldung_form'),
)
