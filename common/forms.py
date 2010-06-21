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


class DeleteForm(forms.Form):
    """
    Useful for confirmation page on which you ask user if he is
    sure he wants to delete some object.

    next field is optional, you can use it to store the URL to which
    user will be redirected after object deletion.
    """

    next = forms.CharField(required=False, widget=forms.HiddenInput)
