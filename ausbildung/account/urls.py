from django.conf.urls import patterns, url, include

from .forms import EmailAuthenticationForm

urlpatterns = patterns('ausbildung.account.views',
    url(r'^$', 'account', name="account"),

    url(r'^register/$',
        'registration',
        name='registration'),
    url(r'^register/(?P<code>[^/]+)/$',
        'registration_confirm',
        name='registration_confirm'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {
        'template_name': 'account/login.html',
        'authentication_form': EmailAuthenticationForm
    }, name='login'),
    url(r'', include('django.contrib.auth.urls')),
)

# Overwriten login
