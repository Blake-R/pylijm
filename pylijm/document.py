# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from collections import Mapping

from six import add_metaclass

from abc import ABCMeta
from pylijm.metacls import DocumentMCS, document_init, values_field


@add_metaclass(DocumentMCS.with_other(ABCMeta))
class Document(Mapping):
    """
    :type __options__: dict[options.Option, object]
    :type __defaults__: dict[str, object]
    :type __fields__: dict[str, field.Field]
    :type __values__: dict[str, object]
    """

    def __init__(self, dict_to_wrap=None, *args, **init_values):
        document_init(self, dict_to_wrap, init_values)
        if args or init_values:
            raise AttributeError('Unexpected values: %r, %r'
                               % (dict(enumerate(args)), init_values))
        super(Document, self).__init__()

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.__values__)

    def __getitem__(self, key):
        return getattr(self, values_field)[key]

    def __iter__(self):
        return iter(getattr(self, values_field))

    def __len__(self):
        return len(getattr(self, values_field))

Mapping.register(Document)


__all__ = ['Document']
