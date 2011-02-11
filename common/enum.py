# -*- coding: utf-8 -*-
"""
This module provides ``Enum`` class which simplifies work with enumerated list of choices.
This implementation is specially developed for use in django models.
"""

import re
import random

class Item(int):
    def __new__(cls, value, label=None):
        obj =  int.__new__(cls, value)
        obj.value = value
        if label is None:
            obj.label = str(obj)
        else:
            obj.label = label
        return obj


def items_from_choices(choices):
    """
    Create dict of enum.Item objects from given values.
    Args:
        choices: dict (key->value) or list of pairs [(value, key), ...]
    """

    items = {}
    if isinstance(choices, dict):
        choices = [(y, x) for x, y in choices.items()]
    for value, label in choices:
        key = label.replace(' ', '_').replace('-', '_')
        key = re.sub(r'_+', '_', key)
        rex = re.compile(r'^[a-z0-9_]*$', re.I)
        if not rex.match(key):
            raise Exception('Could not create key from label: %s' % label)
        items[key] = Item(value, label)
    return items


class MetaEnum(type):
    """
    Find all enum.Item attributes and save them into ``_items`` attribute.
    """

    def __new__(cls, name, bases, attrs):
        items = {}
        for base in bases:
            if isinstance(base, MetaEnum):
                items.update(base._items)
        if '_choices' in attrs:
            attrs.update(items_from_choices(attrs['_choices']))
            del attrs['_choices']
        for key, attr in attrs.items():
            if isinstance(attr, Item):
                attr.key = key
                items[key] = attr
                del attrs[key]
        attrs['_items'] = items
        return type.__new__(cls, name, bases, attrs)

    """
    Public methods:
    """

    def by_value(cls, value):
        """
        Return enum.Item which has the given value.
        """

        return [x for x in cls._items.itervalues() if x.value == value][0]

    def by_key(cls, key):
        """
        Return enum.Item which has the given key.
        """

        return cls._items[key]

    def __iter__(cls):
        """
        Iterate over tuples of (value, label)
        """

        return iter(cls.choices())

    def __len__(self):
        """
        Return the number of enum.Item objects.
        """

        return len(self._items)

    def choices(cls):
        """
        Return tuples of (value, label) for all enum.Item objects.
        """

        return [(x.value, x.label) for x in cls._items.itervalues()]

    def values(self):
        """
        Return list of values of all enum.Item objects.
        """

        return self._items.values()

    def random_value(cls):
        """
        Return random value of enum.Item object.
        """

        return random.choice(cls._items.values())

    """
    Private methods:
    """

    def __getattribute__(self, key):
        """
        Each enum.Item object could be accessed as enum.Enum instance's attribute.
        """

        items = type.__getattribute__(self, '_items')
        if key in items:
            return items[key]
        else:
            return type.__getattribute__(self, key)


class Enum(object):
    __metaclass__ = MetaEnum


def build(choices):
    class _Enum(Enum):
        _choices = choices
    return _Enum


if __name__ == '__main__':
    import sys
    enum = sys.modules['__main__']
    class Body(enum.Enum):
        sedan = enum.Item(1, u'Sedan')
        hatchback = enum.Item(2, u'Hatchback')

    assert set(Body) == set([(1, u'Sedan'), (2, u'Hatchback')])
    assert Body.sedan == 1

    Body = enum.build(((1, u'Sedan'), (2, u'Hatchback')))
    assert set(Body) == set([(1, u'Sedan'), (2, u'Hatchback')])

    class Body(enum.Enum):
        _choices = ((1, u'Sedan'), (2, u'Hatchback'))
    assert set(Body) == set([(1, u'Sedan'), (2, u'Hatchback')])

    class Body(enum.Enum):
        _choices = dict(Sedan=1, Hatchback=2)
    assert set(Body) == set([(1, u'Sedan'), (2, u'Hatchback')])

    assert Body.by_value(1).key == 'Sedan'

    print 'Done'
