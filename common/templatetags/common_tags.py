# -*- coding: utf-8
from cgi import parse_qsl
from urllib import urlencode

from django import template
from django.utils.encoding import smart_str


register = template.Library()

@register.simple_tag
def alter_qs(qs, name, value, name2=None, value2=None):
    """
    Alter query string argument with new value.
    """

    qs = qs.lstrip('?')
    args = dict((x[0], smart_str(x[1])) for x in parse_qsl(qs))
    if value:
        args[name] = smart_str(value)
    else:
        if name in args:
            del args[name]
    if args:
        result = '?' + urlencode(args)
        if name2 and value2:
            return alter_qs(result, name2, value2)
        else:
            return result
    else:
        return ''
