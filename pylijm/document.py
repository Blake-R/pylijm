# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from six import add_metaclass, iterkeys

from pylijm.metacls import DocumentMCS, document_init, document_update


@add_metaclass(DocumentMCS)
class Document(dict):
    """
    :type __options__: dict[pylijm.options.Option, object]
    :type __defaults__: dict[str, any]
    :type __fields__: dict[str, pylijm.field.Field]
    :type __values__: dict[str, any]
    """

    @property
    def dict(self):
        return {}  # Wrapped in metaclass.

    def __init__(self, dict_to_wrap=None, *args, **init_values):
        # TODO: Make Document class wrap dict instead make it copy.
        values = document_init(self, dict_to_wrap, init_values)
        if args or init_values:
            raise AttributeError('Unexpected arguments: %r, %r'
                                 % (dict(enumerate(args)), init_values))
        super(Document, self).__init__(values)

    def clear(self):
        for k in iterkeys(self.dict):
            delattr(self, k)

    def copy(self):
        return type(self)(self)

    '''
    @staticmethod
    def fromkeys(s, v=None):
        raise NotImplementedError()

    def get(self, k, d=None):
        return self.dict.get(k, d)

    def has_key(self, k):
        return k in self.dict

    def items(self):
        return self.dict.items()

    if PY2:
        def iteritems(self):
            return self.dict.iteritems()

        def iterkeys(self):
            return self.dict.iterkeys()

        def itervalues(self):
            return self.dict.itervalues()

    def keys(self):
        return self.dict.keys()
    '''

    def pop(self, k, d=None):
        r = self.dict.get(k, d)
        delattr(self, k)
        return r

    def popitem(self):
        raise NotImplementedError()

    def setdefault(self, k, d=None):
        r = self.dict[k]
        if r is None:
            r = d
            setattr(self, k, d)
        return r

    def update(self, dict_for_update=None, **update_values):
        document_update(self, dict_for_update, update_values)
        if update_values:
            raise AttributeError('Unexpected arguments: %r'
                                  % (update_values,))

    '''
    def values(self):
        return self.dict.values()

    if PY2:
        def viewitems(self):
            return self.dict.viewitems()

        def viewkeys(self):
            return self.dict.viewkeys()

        def viewvalues(self):
            return self.dict.viewvalues()

    def __cmp__(self, y):
        return self.dict.__cmp__(y)

    def __contains__(self, k):
        return k in self.dict
    '''

    def __delitem__(self, k):
        delattr(self, k)

    '''
    def __eq__(self, y):
        return self.dict.__eq__(y)

    def __getitem__(self, key):
        return self.dict[key]

    def __ge__(self, y):
        return self.dict.__ge__(y)

    def __gt__(self, y):
        return self.dict.__gt__(y)

    def __iter__(self):
        return self.dict.__iter__()

    def __len__(self):
        return len(self.dict)

    def __le__(self, y):
        return self.dict.__le__(y)

    def __lt__(self, y):
        return self.dict.__lt__(y)

    def __ne__(self, y):
        return self.dict.__ne__(y)
    '''

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, dict.__repr__(self))

    def __setitem__(self, k, v):
        setattr(self, k, v)

    '''
    def __sizeof__(self):
        return object.__sizeof__(self)
    '''


__all__ = ['Document']
