import os
import sys

_ = lambda x: x

WEBAPP_DIR = os.path.dirname(os.path.abspath(__file__))
APP_BASEDIR = os.path.abspath(os.path.join(WEBAPP_DIR, os.path.pardir))
DEBUG = 'runserver' in sys.argv
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['localhost', '.aure4.ch']

ADMINS = (
    ('Stefan Reinhard / Chili', 'chili@gloggi.ch'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(APP_BASEDIR, 'dev.db'),
    }
}

TIME_ZONE = 'Europe/Zurich'

LANGUAGE_CODE = 'de-CH'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = False

LANGUAGES = (('de', _('German')),)

SECRET_KEY = 'not_so_secret'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

MEDIA_ROOT = os.path.join(APP_BASEDIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(APP_BASEDIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(APP_BASEDIR, 'ausbildung', 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ausbildung.urls'

WSGI_APPLICATION = 'ausbildung.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(APP_BASEDIR, 'ausbildung', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request'
)

INSTALLED_APPS = (
    'suit',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'feincms',
    'feincms.module.page',
    'feincms.module.medialibrary',
    'tinymce',
    'south',
    'gunicorn',
    'sorl.thumbnail',
    'reversion',
    'report_builder',

    'ausbildung',
    'ausbildung.account',
    'ausbildung.anmeldung',
)

SOUTH_MIGRATION_MODULES = {
    'page': 'ausbildung.migrate.page',
    'medialibrary': 'ausbildung.migrate.medialibrary',
}

AUTHENTICATION_BACKENDS = (
    'ausbildung.account.backend.EmailBackend',
    'django.contrib.auth.backends.ModelBackend'
)

LOGIN_URL = '/account/'
LOGOUT_URL = '/account/logout/'

FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': STATIC_URL + '/tiny_mce/tiny_mce.js',
}

SERVER_EMAIL = 'anmeldung@aure4.ch'
DEFAULT_FROM_EMAIL = 'anmeldung@aure4.ch'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SUIT_CONFIG = {
    'ADMIN_NAME': 'AURE 4 admin'
}

try:
    from ausbildung.local_settings import *
except ImportError:
    pass