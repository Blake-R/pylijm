# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from six import text_type
from unittest2 import TestCase

from pylijm.dict import Dict


class TestDict(TestCase):
    @property
    def fixture(self):
        return Dict(text_type, int)

    def test_init_good(self):
        Fix = self.fixture
        self.assertDictEqual({}, Fix())
        self.assertDictEqual({'test': 0}, Fix(test=0))
        self.assertDictEqual({'test': 0}, Fix(test='0'))
        self.assertDictEqual({'test': 0}, Fix({'test': '0'}))
        self.assertDictEqual({'0': 0}, Fix({0: 0}))

    def test_init_bad(self):
        Fix = self.fixture
        self.assertRaises(TypeError, Fix, test=None)
        self.assertRaises(TypeError, Fix, test=dict())
        self.assertRaises(ValueError, Fix, {None: 0})

    def test_set(self):
        fix = self.fixture()
        fix['test'] = 0
        self.assertEqual(0, fix['test'])
        with self.assertRaises(TypeError):
            fix[None] = 0
        with self.assertRaises(TypeError):
            fix[0] = 0

    def test_unset(self):
        fix = self.fixture({0: 0}, test=0)
        del fix['test']
        with self.assertRaises(KeyError):
            del fix[None]
        with self.assertRaises(KeyError):
            del fix[0]
