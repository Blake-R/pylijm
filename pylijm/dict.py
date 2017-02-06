# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from abc import ABCMeta, abstractproperty

from six import iterkeys


def Dict(ktypes, vtypes):
    ktypes = ensure_format(ktypes)
    vtypes = ensure_format(vtypes)

    class _Dict(DictBase):
        __slots__ = ()

        @property
        def key_types(self):
            return ktypes

        @property
        def value_types(self):
            return vtypes
    _Dict.__name__ = 'Dict'
    return _Dict


class DictBase(dict):
    __metaclass__ = ABCMeta
    __slots__ = ()

    @abstractproperty
    def key_types(self):
        raise NotImplementedError()

    @abstractproperty
    def value_types(self):
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        super(DictBase, self).__init__(*args, **kwargs)
        self.convert_dict(self)

    def convert_dict(self, d):
        for n in iterkeys(d):
            k = self.cast_key(n)
            v = self.cast_value(d[n])
            if k is not n:
                del d[n]
            d[k] = v

    def checked_key(self, key):
        if not isinstance(key, self.key_types):
            raise TypeError((key, type(key), self.key_types))
        return key

    def checked_value(self, value):
        if not isinstance(value, self.value_types):
            raise TypeError((value, type(value), self.value_types))
        return value

    def cast_key(self, key):
        if not isinstance(key, self.key_types):
            if key is None:
                raise ValueError((key, type(key)))
            key = self.key_types[0](key)
        return key

    def cast_value(self, value):
        if not isinstance(value, self.value_types):
            value = self.value_types[0](value)
        return value

    def __setitem__(self, key, value):
        key = self.checked_key(key)
        value = self.checked_value(value)
        super(DictBase, self).__setitem__(key, value)

    def setdefault(self, k, d=None):
        if k not in self:
            k = self.checked_key(k)
            self[k] = self.checked_value(d)
        return self[k]

    def update(self, *args, **kw):
        d = dict(*args, **kw)
        self.convert_dict(d)
        super(DictBase, self).update(d)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, super(DictBase, self).__repr__())


def ensure_format(types):
    if not isinstance(types, tuple):
        types = (types,)
    assert any(isinstance(x, type) for x in types), types
    return types
