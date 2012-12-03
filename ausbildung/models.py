# encoding: utf-8

from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.section.models import SectionContent
from feincms.content.medialibrary.v2 import MediaFileContent

from feincms_cleanse import cleanse_html

from BeautifulSoup import BeautifulSoup

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

# Patch Section content to support cleanse and save anchors on headings
def save(self, *args, **kwargs):
    if getattr(self, 'cleanse', False):
        try:
            self.richtext = self.cleanse(self.richtext)
        except TypeError:
            self.richtext = self.cleanse.im_func(self.richtext)

    if not self.id:
        super(SectionContent, self).save(*args, **kwargs)

    soup = BeautifulSoup(self.richtext)
    for i, h3 in enumerate(soup.findAll('h3')):
        h3['id'] = u'section%d.%d' % (self.id, i + 1)

    self.richtext = soup.prettify()

    super(SectionContent, self).save(*args, **kwargs)

SectionContent.save = save

Page.create_content_type(RichTextContent, cleanse=cleanse_html)
Page.create_content_type(SectionContent, cleanse=cleanse_html, TYPE_CHOICES=(
     ('menu', 'Mit Menü'),
))
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
