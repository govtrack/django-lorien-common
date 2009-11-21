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


# TODO: refactor this code, move it to common.pagination module
# TODO: this old code requires refactoring
@register.inclusion_tag('common/pagination.html',takes_context=True)
def pagination(context, adjacent_pages=5):
    """
    Return the list of A tags with links to pages.
    """

    page_list = range(
        max(1,context['page'] - adjacent_pages),
        min(context['pages'],context['page'] + adjacent_pages) + 1)
    lower_page = None
    higher_page = None

    if not 1 == context['page']:
        lower_page = context['page'] - 1

    if not 1 in page_list:
        page_list.insert(0,1)
        if not 2 in page_list:
            page_list.insert(1,'.')

    if not context['pages'] == context['page']:
        higher_page = context['page'] + 1

    if not context['pages'] in page_list:
        if not context['pages'] - 1 in page_list:
            page_list.append('.')
        page_list.append(context['pages'])
    get_params = '&'.join(['%s=%s' % (x[0],''.join(x[1])) for x in
        context['request'].GET.iteritems() if (not x[0] == 'page' and not x[0] == 'per_page')])
    if get_params:
        get_params = '?%s&' % get_params
    else:
        get_params = '?'

    return {
        'get_params': get_params,
        'lower_page': lower_page,
        'higher_page': higher_page,
        'page': context['page'],
        'pages': context['pages'],
        'page_list': page_list,
        'per_page': context['per_page'],
        }
