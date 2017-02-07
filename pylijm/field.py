# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy
from sys import exc_info

from six import reraise


class NoDefaultValueClass(object):
    def __repr__(self):
        return 'NoDefaultValue'
NoDefaultValue = NoDefaultValueClass()


class Field(object):
    __slots__ = ('_name', '_fullname', '_type', '_default')

    @property
    def name(self):
        return self._name

    @property
    def fullname(self):
        return self._fullname

    @property
    def type(self):
        return self._type

    @property
    def default(self):
        if self._default is NoDefaultValue:
            raise ValueError('Field "%s" does not have default value' % self.fullname)
        if callable(self._default):
            return self._default()
        return deepcopy(self._default)

    def __init__(self, modelname, name, ftype, default):
        super(Field, self).__init__()
        self._name = name
        self._fullname = '.'.join((modelname, self._name))
        self._type = ftype
        self._default = default

    def cast(self, value):
        if value is None:
            return self.default
        if not self.is_type(value):
            try:
                value = self._type(value)
            except BaseException as e:
                z = TypeError('Cast failed for %s: %r' % (self.fullname, e))
                z.__name__ = type(e).__name__
                reraise(None, z, exc_info()[2])
        return value

    def is_type(self, value):
        return isinstance(value, self._type)

    def checked(self, value):
        if self.is_type(value):
            return value
        tv, tf = type(value).__name__, self._type.__name__
        if tv == tf:
            tv = '.'.join((type(value).__module__, tv))
            tf = '.'.join((type(value).__module__, tf))
        raise TypeError('Type for field "%s" value should be "%s", got "%s"' % (self.fullname, tf, tv))

    def __repr__(self):
        if self._type.__module__ == '__builtin__':
            t = self._type.__name__
        else:
            t = '.'.join((self._type.__module__, self._type.__name__))
        return '%s(type=%s, default=%r)' % (self.fullname, t, self._default)

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        try:
            return dict.__getitem__(instance, self._name)
        except KeyError:
            reraise(None, AttributeError(self.name), exc_info()[2])

    def __set__(self, instance, value):
        dict.__setitem__(instance, self._name, self.checked(value))

    def __delete__(self, instance):
        if self._default is NoDefaultValue:
            raise AttributeError('You should not delete field "%s" without default value' % self._name)
        dict.__setitem__(instance, self._name, self.default)
