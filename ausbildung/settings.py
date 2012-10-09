import os
import sys
import dj_database_url

WEBAPP_DIR = os.path.dirname(os.path.abspath(__file__))
APP_BASEDIR = os.path.abspath(os.path.join(WEBAPP_DIR, os.path.pardir))
DEBUG = any((cmd in sys.argv for cmd in (
    'runserver', 'shell', 'dbshell', 'sql', 'sqlall')))
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Gloggi Admin', 'admin@gloggi.ch'),
)

MANAGERS = ADMINS

#DATABASES = {'default': {
#    'ENGINE': 'django.db.backends.sqlite3',
#    'NAME': ,
#    'USER': '',
#    'PASSWORD': '',
#    'HOST': '',
#    'PORT': '',
#}}

DEV_DB = os.path.join(APP_BASEDIR, 'dev.db')

DATABASES = {'default': dj_database_url.config(default='sqlite:///%s' % DEV_DB)}

TIME_ZONE = 'Europe/Zurich'

LANGUAGE_CODE = 'de-CH'

SITE_ID = 1

USE_I18N = False
USE_L10N = False
USE_TZ = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ['S3_KEY']
AWS_SECRET_ACCESS_KEY = os.environ['S3_SECRET']
AWS_STORAGE_BUCKET_NAME = 'gloggiausbildung'

#MEDIA_ROOT = os.path.join(APP_BASEDIR, 'uploads')
#MEDIA_URL = '/uploads/'

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
    'django.contrib.messages.middleware.MessageMiddleware',
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
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'feincms',
    'feincms.module.page',
    'feincms.module.medialibrary',
    'fhadmin',
    'tinymce',
    'south',
    'gunicorn',

    'ausbildung',
)

FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': STATIC_URL + '/tiny_mce/tiny_mce.js',
}

from fhadmin import FHADMIN_GROUPS_REMAINING
_ = lambda x: x

FHADMIN_GROUPS_CONFIG = [
    (_('Main content'), {
        'apps': ('page', 'medialibrary', 'blog'),
        }),
    (_('Modules'), {
        'apps': ('links', FHADMIN_GROUPS_REMAINING),
        }),
    (_('Preferences'), {
        'apps': ('auth', 'rosetta', 'external', 'sites'),
        }),
    ]
