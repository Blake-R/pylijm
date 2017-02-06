# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


class Option(object):
    __slots__ = ()


allows_semiprivate_fields = Option()


defaults = {
    allows_semiprivate_fields: False
}
