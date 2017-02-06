# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from abc import ABCMeta
from collections import Mapping

from six import add_metaclass

from pylijm.dockbase import DocumentBase
from pylijm.metacls import DocumentMCS


@add_metaclass(DocumentMCS.with_other(ABCMeta))
class Document(DocumentBase):
    """
    :type __options__: dict[options.Option, object]
    :type __defaults__: dict[str, object]
    :type __fields__: dict[str, field.Field]
    :type __values__: dict[str, object]
    """

    @property
    def dict(self):
        return {}  # Wrapped in metaclass.

    def __init__(self, dict_to_wrap=None, *args, **init_values):
        super(Document, self).__init__() # Wrapped in metaclass.

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.dict)

    def __getitem__(self, key):
        return self.dict[key]

    def __iter__(self):
        return self.dict.__iter__()

    def __len__(self):
        return len(self.dict)

Mapping.register(Document)


__all__ = ['Document']
