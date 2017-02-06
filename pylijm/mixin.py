# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


class AsDictMixin(object):
    def as_dict_(self):
        raise NotImplementedError()
