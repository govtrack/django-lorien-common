# -*- coding: utf-8 -*-
"""
This module provides ``List`` class which simplifies work with enumerated list of choices.
This implementation is specially developed for use in django models.
"""

import re

class Item(object):
    def __init__(self, key=None, label=None):
        self.key = key
        self.label = key if label is None else label


class MetaList(type):
    """
    Find all enum.Item attributes and save them into ``items`` attribute.
    """

    def __new__(cls, name, bases, attrs):
        items = {}
        for key, attr in attrs.items():
            if isinstance(attr, Item):
                items[key] = attr
                attr.slug = key
                attrs[key] = attr.key
        new_cls = type.__new__(cls, name, bases, attrs)
        new_cls.items = items
        return new_cls

    def get_choices(cls):
        return ((x.key, x.label) for x in cls.items.itervalues())

    def __iter__(cls):
        return iter(cls.get_choices())

    def update_choices(cls, choices):
        for key in cls.items:
            delattr(cls, key)
        items = {}
        for choice in choices:
            if len(choice) == 3:
                key, label, attrname = choice
            else:
                key, label = choice

                attrname = label.replace(' ', '_').replace('-', '_')
                rex = re.compile(r'^[a-z][a-z0-9_]*$', re.I)
                if not rex.match(attrname):
                    raise Exception('Could not create attribute name from label: %s' % label)
            items[attrname] = Item(key, label)
            setattr(cls, attrname, key)
        cls.items = items

    def item_by_value(self, value):
        return [x for x in self.items.itervalues() if x.key == value][0]

    def get_by_slug(self, slug):
        return self.items[slug].key


class List(object):
    __metaclass__ = MetaList

    def __init__(self, choices=None):
        if choices is not None:
            self.update_choices(choices)


def from_choices(choices):
    class _List(List):
        pass
    _List.update_choices(choices)
    return _List


if __name__ == '__main__':
    import sys
    enum = sys.modules['__main__']
    class Body(enum.List):
        sedan = enum.Item(1, u'Sedan')
        hatchback = enum.Item(2, u'Hatchback')

    assert set(Body) == set([(1, u'Sedan'), (2, u'Hatchback')])
    assert Body.sedan == 1

    Body = enum.from_choices(((1, u'Sedan'), (2, u'Hatchback'), (3, u'Уаз', 'Uaz')))
    assert set(Body) == set([(1, u'Sedan'), (2, u'Hatchback'), (3, u'Уаз')])
    assert Body.Uaz == 3

    print 'Done'
