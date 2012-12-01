from django.conf.urls import patterns, url, include

from .forms import EmailAuthenticationForm

urlpatterns = patterns('ausbildung.account.views',
    url(r'^$', 'account', name="account"),

    url(r'^signup/$', 'signup', name="signup"),
    url(r'^email_register/', include('email_registration.urls')),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {
        'template_name': 'account/login.html',
        'authentication_form': EmailAuthenticationForm
    }, name='login'),
    url(r'', include('django.contrib.auth.urls')),
)

# Overwriten login
