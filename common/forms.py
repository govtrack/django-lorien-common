# -*- coding: utf-8 -*-
from django import forms

def build_form(Form, _request, *args, **kwargs):
    """
    Shorcut for building the form instance of given class.
    """

    if 'POST' == _request.method:
        form = Form(_request.POST, _request.FILES, *args, **kwargs)
    else:
        form = Form(*args, **kwargs)
    return form
