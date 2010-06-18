from urlparse import urlsplit

from django.conf import settings
from django.views.static import serve

PREFIX = urlsplit(settings.MEDIA_URL).path

class StaticFilesMiddleware(object):
    """
    Django middleware for serving static files instead of using urls.py
    """

    def process_request(self, request):
        if settings.DEBUG:
            if request.path.startswith(PREFIX):
                path = request.path[len(PREFIX):]
                return serve(request, path, settings.MEDIA_ROOT)
