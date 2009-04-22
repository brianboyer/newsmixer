from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter()
@stringfilter
def js_string(value):
    import re
    return re.sub(r'[\r\n]+','',value)