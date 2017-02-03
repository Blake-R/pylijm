# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from six import add_metaclass, iteritems

from .metacls import DocumentMCS, document_init


@add_metaclass(DocumentMCS)
class Document(object):
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
        a = ['%s=%s' % x for x in iteritems(self.__values__)]
        return '%s(%s)' % (type(self).__name__, ', '.join(a))


__all__ = ['Document']
