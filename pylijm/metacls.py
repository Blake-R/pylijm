# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

from six import iteritems, PY2

from pylijm import options as opts
from pylijm.defs import *
from pylijm.defs import dict_property
from pylijm.field import Field, NoDefaultValue


_multimetas = {}


class DocumentMCS(type):
    @staticmethod
    def with_other(other, *others):
        all_clss = (DocumentMCS, other) + others
        multimetaname = ','.join(sorted((x.__name__ for x in all_clss)))
        if multimetaname in _multimetas:
            return _multimetas[multimetaname]
        multimetacls = type(b'DocumentMultiMCS' if PY2 else 'DocumentMultiMCS', all_clss, {})
        _multimetas[multimetaname] = multimetacls
        return multimetacls

    def __new__(mcs, what, bases, dict_):
        """
        :param str what:
        :param tuple bases:
        :param dict dict_:
        """
        options = opts.defaults.copy()
        defaults = {}
        fields = OrderedDict()

        for b in bases:
            if hasattr(b, defaults_field):
                defaults.update(getattr(b, defaults_field))
            if hasattr(b, options_field):
                options.update(getattr(b, options_field))
            if hasattr(b, fields_field):
                fields.update(getattr(b, fields_field))

        if defaults_field in dict_:
            defaults.update(dict_[defaults_field])
        if options_field in dict_:
            options.update(dict_[options_field])
        if fields_field in dict_:
            raise TypeError('New document type %s should not have member %s'
                            % (what, fields_field))
        if values_field in dict_:
            raise TypeError('New document type %s should not have member %s'
                            % (what, values_field))

        private_prefix = '__' if options[opts.allows_semiprivate_fields] else '_'

        for name, ftype in iteritems(dict_):
            if name.startswith(private_prefix):
                continue
            if not isinstance(ftype, type):
                continue
            default = defaults.pop(name, NoDefaultValue)
            fields[name] = Field(what, name, ftype, default)

        if defaults:
            raise RuntimeError('%s have unknown fields in defaults: %r'
                               % (what, defaults))

        dict_.update(fields)
        dict_[options_field] = options
        dict_[defaults_field] = defaults
        dict_[fields_field] = fields
        dict_[dict_property] = property(lambda d: d) # property(get_values_field)

        return super(DocumentMCS, mcs).__new__(mcs, what, bases, dict_)

    def __delattr__(cls, name):
        if name in getattr(cls, fields_field):
            raise AttributeError('You should not delete fields')
        if name in all_fields:
            raise AttributeError('You should not delete special members')
        super(DocumentMCS, cls).__delattr__(name)

    def __setattr__(cls, name, value):
        if name in getattr(cls, fields_field):
            raise AttributeError('You should not change fields')
        if name in all_fields:
            raise AttributeError('You should not change special members')
        if isinstance(value, Field):
            raise AttributeError('You should not add new fields')
        super(DocumentMCS, cls).__setattr__(name, value)


def document_init(self, dict_to_wrap, init_values):
    dict_to_wrap = dict_to_wrap or {}
    cls = type(self)
    fields = getattr(cls, fields_field)
    values = {}

    excess_keys = set(values).difference(fields)
    if excess_keys:
        raise AttributeError('%s.%s excess keys found: %s'
                             % (cls.__module__, cls.__name__, excess_keys))

    for k, f in iteritems(fields):
        if k in init_values:
            values[k] = f.checked(init_values.pop(k))
        elif k not in dict_to_wrap:
            values[k] = f.default
        else:
            v = dict_to_wrap[k]
            if not isinstance(v, f.type):
                values[k] = f.cast(v)
            else:
                values[k] = v

    return values


def document_update(self, dict_for_update, update_values):
    cls = type(self)
    fields = getattr(cls, fields_field)
    dict_for_update = dict_for_update or {}

    excess_keys = set(dict_for_update).difference(fields)
    if excess_keys:
        raise AttributeError('%s.%s excess keys found: %s'
                             % (cls.__module__, cls.__name__, excess_keys))

    for k, f in iteritems(fields):
        if k in update_values:
            v = f.checked(update_values[k])
        elif k in dict_for_update:
            v = f.cast(dict_for_update[k])
        else:
            continue
        setattr(self, k, v)


def get_values_field(self):
    return getattr(self, values_field)
