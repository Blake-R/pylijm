# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from unittest2 import TestCase

from pylijm.list import List


class TestDict(TestCase):
    @property
    def fixture(self):
        return List(int)

    def test_init_good(self):
        Fix = self.fixture
        self.assertListEqual([], Fix())
        self.assertListEqual([0], Fix([0]))
        self.assertListEqual([0], Fix(['0']))

    def test_init_bad(self):
        Fix = self.fixture
        self.assertRaises(TypeError, Fix, [None])
        self.assertRaises(TypeError, Fix, [dict()])

    def test_set(self):
        fix = self.fixture([0])
        fix[0] = 1
        self.assertEqual(1, fix[0])
        with self.assertRaises(TypeError):
            fix[None] = 0
        with self.assertRaises(TypeError):
            fix['0'] = 0

    def test_unset(self):
        fix = self.fixture([0])
        del fix[0]
        with self.assertRaises(TypeError):
            del fix[None]
        with self.assertRaises(TypeError):
            del fix['0']
