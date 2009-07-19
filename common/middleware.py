# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect

class LoginRequiredMiddleware(object):
    """
    This middleware restrict access to site for not authenticated users.

    It allows access to views from settings.PUBLIC_REFIXES list.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        for public_prefix in settings.PUBLIC_PREFIXES:
            if request.path.startswith(public_prefix):
                return None
        if not request.user.is_authenticated():
            return HttpResponseRedirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return None
