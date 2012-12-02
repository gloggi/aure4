# encoding: utf-8

from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.section.models import SectionContent
from feincms.content.medialibrary.v2 import MediaFileContent

Page.register_extensions()

Page.register_templates({
    'title': _('Standard'),
    'path': 'feincms_main.html',
    'regions': (
        ('main', _('Main')),
    ),
}, {
    'title': _('2 Spalten'),
    'path': 'feincms_side.html',
    'regions': (
        ('main', _('Main')),
        ('side', _('Sidebar'))
    ),
})

Page.register_extensions('titles')

Page.create_content_type(RichTextContent)
Page.create_content_type(SectionContent, TYPE_CHOICES=(
     ('menu', 'Mit Menü'),
))
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
