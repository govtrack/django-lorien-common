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
    args = [[x[0], smart_str(x[1])] for x in parse_qsl(qs)]
    if value:
        found = False
        for arg in args:
            if arg[0] == name:
                arg[1] = smart_str(value)
                found = True
        if not found:
            args.append([name, smart_str(value)])
    else:
        args = [x for x in args if x[0] != name]
    if args:
        args = [tuple(x) for x in args]
        result = '?' + urlencode(args)
        if name2 and value2:
            return alter_qs(result, name2, value2)
        else:
            return result
    else:
        return ''
