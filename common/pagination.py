from django.core.paginator import Paginator, EmptyPage, InvalidPage

from common.templatetags.common_tags import alter_qs


def paginate(qs, request, per_page=15, frame_size=None):
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

    page.first_page_url = alter_qs(query_string, 'page', 1)
    page.last_page_url = alter_qs(query_string, 'page', page.paginator.num_pages)

    urls = []
    if frame_size is None:
        for x in page.paginator.page_range:
            urls.append((x, alter_qs(query_string, 'page', x)))
    else:
        half = int(frame_size / 2.0)
        start = max(1, page.number - int(frame_size / 2.0))
        stop = min(page.paginator.num_pages, page.number + (frame_size - half))
        if start > 1:
            urls.append((None, None))
        for x in xrange(start, stop):
            urls.append((x, alter_qs(query_string, 'page', x)))
        if stop < page.paginator.num_pages:
            urls.append((None, None))
    page.paginator.page_range_urls = urls

    return page
