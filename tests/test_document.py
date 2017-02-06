# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json

from six import text_type
from unittest2 import TestCase

from pylijm.document import Document


class TestDocument(TestCase):
    @property
    def fixture(self):
        class Sub(Document):
            sub = text_type

        class Fix(Document):
            test = int
            defl = int
            sub = Sub
            __defaults__ = {
                'defl': 0,
                'sub': Sub(sub='test')
            }
        return Fix

    def test_cls_struct_change(self):
        Fix = self.fixture
        with self.assertRaises(AttributeError):
            del Fix.test
        with self.assertRaises(AttributeError):
            Fix.test = Fix.test

    def test_init_good(self):
        Fix = self.fixture
        self.assertEqual(0, Fix(test=0).test)
        self.assertEqual(0, Fix({'test': 0}).test)
        self.assertEqual(0, Fix({'test': False}).test)
        self.assertEqual(0, Fix({'test': '0'}).test)
        self.assertEqual(0, Fix({'test': 0, 'defl': None}).defl)

    def test_init_bad(self):
        Fix = self.fixture
        self.assertRaises(ValueError, Fix)
        self.assertRaises(ValueError, Fix, {})
        self.assertRaises(TypeError, Fix, test=None)
        self.assertRaises(TypeError, Fix, test='0')
        self.assertRaises(AttributeError, Fix, test=0, undefined=0)
        self.assertRaises(ValueError, Fix, {'test': None})
        self.assertRaises(TypeError, Fix, {'test': dict()})
        self.assertRaises(TypeError, Fix, test=0, defl=None)
        self.assertRaises(TypeError, Fix, {'test': 0, 'defl': dict()})

    def test_set_good(self):
        fix = self.fixture(test=0)
        fix.test += 1
        fix.defl += 1
        self.assertEqual(1, fix.test)
        self.assertEqual(1, fix.defl)

    def test_set_bad(self):
        fix = self.fixture(test=1)
        with self.assertRaises(TypeError):
            fix.test = None
        with self.assertRaises(TypeError):
            fix.defl = None
        with self.assertRaises(TypeError):
            fix.test = '1'

    def test_unset(self):
        fix = self.fixture(test=0)
        fix.defl += 1
        self.assertEqual(1, fix.defl)
        del fix.defl
        self.assertEqual(0, fix.defl)
        with self.assertRaises(AttributeError):
            del fix.test

    def test_as_dict(self):
        fix = self.fixture(test=1)
        self.assertIsInstance(fix, dict)
        js = json.loads(json.dumps(fix))
        self.assertDictEqual(js, fix)

    def test_dict_consistent(self):
        d = {'test': 1, 'defl': 1}
        fix = self.fixture(d)
        self.assertEqual(id(d), id(fix.dict))
        self.assertIn('sub', fix.dict)
