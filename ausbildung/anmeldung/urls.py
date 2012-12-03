from django.conf.urls import patterns, url

urlpatterns = patterns('ausbildung.anmeldung.views',
    url(r'^$', 'kurse',
        name='anmeldung_kurse'),
    url(r'^(?P<kurs>[-\w]+)/$', 'anmeldung',
        name='anmeldung_form'),
    url(r'^(?P<kurs>[-\w]+)/view/$', 'anmeldung_view',
        name='anmeldung_view'),
)
