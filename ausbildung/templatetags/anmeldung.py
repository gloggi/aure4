from django import template


register = template.Library()


@register.filter()
def printbool(val):
    if val is True or val is False:
        return 'Ja' if val else 'Nein'
    else:
        return val
