from django.core.paginator import Paginator, EmptyPage, InvalidPage

from common.templatetags.common_tags import alter_qs


def paginate(qs, request, per_page=15):
    try:    
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        page_number = 1

    paginator = Paginator(qs, per_page)
    try:    
        page = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        page_number = 1
        page = paginator.page(1)
    query_string = request.META['QUERY_STRING']

    if page.has_previous():
        page.previous_page_url = alter_qs(query_string, 'page', page.previous_page_number())
    else:
        page.previous_page_url = None

    if page.has_next():
        page.next_page_url = alter_qs(query_string, 'page', page.next_page_number())
    else:
        page.next_page_url = None

    page.paginator.page_range_urls = []
    for x in page.paginator.page_range:
        page.paginator.page_range_urls.append((x, alter_qs(query_string, 'page', x)))

    return page
