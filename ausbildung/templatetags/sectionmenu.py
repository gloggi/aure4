from django import template

from BeautifulSoup import BeautifulSoup

register = template.Library()


@register.inclusion_tag('sectionmenu.html')
def sectionmenu(feincms_page):
    menu = []

    for section in feincms_page.sectioncontent_set.all():
        entry = {
            'title': section.title,
            'anchor': u'#section%d' % section.id
        }

        soup = BeautifulSoup(section.richtext)

        subs = soup.findAll('h3')
        if subs:
            subentries = []
            for i, sub in enumerate(subs):
                subentries.append({
                    'title': sub.text,
                    'anchor': u'#section%d.%d' % (section.id, i+1)
                })

            entry['sub'] = subentries

        menu.append(entry)

    return {
        'menu': menu,
    }
