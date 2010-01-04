# -*- coding: utf-8 -*-
import traceback

from django.shortcuts import render_to_response
from django.template import RequestContext

from common.http import HttpResponseJson

def render_to(template):
    """
    Shortcut for rendering template with RequestContext.

    If decorated function returns non dict then just return that result
    else use RequestContext for rendering the template.
    """

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            else:
                ctx = RequestContext(request)
                return render_to_response(template, output, context_instance=ctx)
        return wrapper
    return decorator


def ajax(func):
    """
    Wrap response of view into JSON format.

    Checks request.method is POST. Return error in JSON in other case.
    """

    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            try:
                response = func(request, *args, **kwargs)
            except Exception, ex:
                response = {'error': traceback.format_exc()}
        else:
            response = {'error': {'type': 403, 'message': 'Accepts only POST request'}}
        if isinstance(response, dict):
            return HttpResponseJson(response)
        else:
            return response
    return wrapper
