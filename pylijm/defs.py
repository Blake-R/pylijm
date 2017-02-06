# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


options_field = '__options__'
defaults_field = '__defaults__'
fields_field = '__fields__'
values_field = '__values__'
dict_property = 'dict'

all_fields = {
    options_field,
    defaults_field,
    fields_field,
    values_field,
    dict_property,
}


__all__ = ['options_field', 'defaults_field', 'fields_field', 'values_field',
           'all_fields']
