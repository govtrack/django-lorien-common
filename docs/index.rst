=============
django-common
=============

The django-common package contains things which speed up
the development with django.

Installation
============

* Install ``django-common`` package with ``pip`` or ``easy_install``
* Append ``common`` to the ``settings.INSTALLED_APPS``

Decorators
==========

.. automodule:: common.decorators

.. autofunction:: render_to

.. autofunction:: ajax

Pagination
==========

.. automodule:: common.pagination

.. autofunction:: paginate

Forms
=====

.. automodule:: common.forms

.. autofunction:: build_form

.. autoclass:: DeleteForm()


Model Fields
============

.. automodule:: common.fields

.. autoclass:: AutoOneToOneField()

.. autoclass:: JSONField()

Enum
====

.. automodule:: common.enum

.. autoclass:: AutoOneToOneField()

.. autoclass:: JSONField()
