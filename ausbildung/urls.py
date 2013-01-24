from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('ausbildung.account.urls')),
    url(r'^anmeldung/', include('ausbildung.anmeldung.urls')),
    url(r'^report_builder/', include('report_builder.urls')),
    url(r'', include('feincms.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
else:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    )
