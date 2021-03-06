# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from abc import ABCMeta, abstractproperty

from six import PY2


__cache = {}


def List(vtypes):
    vtypes = ensure_format(vtypes)

    def value_types(self):
        return vtypes

    name = '__'.join(('List', build_types_name(vtypes)))

    if name in __cache:
        return __cache[name]

    t = type(name.encode() if PY2 else name, (ListBase,), {
        'value_types': property(value_types)
    })

    __cache[name] = t

    return t


class ListBase(list):
    __metaclass__ = ABCMeta

    @abstractproperty
    def value_types(self):
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        super(ListBase, self).__init__(*args, **kwargs)
        self.convert_list(self)

    def convert_list(self, l):
        for i, v in enumerate(l):
            l[i] = self.cast_value(v)

    def cast_value(self, value):
        if not isinstance(value, self.value_types):
            value = self.value_types[0](value)
        return value

    def append(self, p_object):
        p_object = self.cast_value(p_object)
        super(ListBase, self).append(p_object)

    def extend(self, iterable):
        l = list(iterable)
        self.convert_list(l)
        super(ListBase, self).extend(l)

    def insert(self, index, p_object):
        p_object = self.cast_value(p_object)
        super(ListBase, self).insert(index, p_object)

    def __add__(self, y):
        r = super(ListBase, self).__add__(y)
        return type(self)(r)

    def __iadd__(self, y):
        y = list(y)
        self.convert_list(y)
        return super(ListBase, self).__iadd__(y)

    def __mul__(self, n):
        r = super(ListBase, self).__mul__(n)
        return type(self)(r)

    def __rmul__(self, n):
        r = super(ListBase, self).__rmul__(n)
        return type(self)(r)

    def __setitem__(self, i, y):
        y = self.cast_value(y)
        super(ListBase, self).__setitem__(i, y)

    def __setslice__(self, i, j, y):
        y = list(y)
        self.convert_list(y)
        super(ListBase, self).__setslice__(i, j, y)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, super(ListBase, self).__repr__())


def ensure_format(types):
    if not isinstance(types, tuple):
        types = (types,)
    assert any(isinstance(x, type) for x in types), types
    return types


def build_types_name(types):
    return '__'.join('_'.join((x.__module__, x.__name__)) for x in types)
