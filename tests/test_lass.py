#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# CONTRIBUTORS (sorted by surname)
# LUO, Pengkui <pengkui.luo@gmail.com>
#
#
# UPDATED ON
# 2013: 04/20, 04/21, 06/11
#
"""
Unit tests

"""
import unittest

from structs import TurboList, LengthAscendingStrings

class Test_LengthAscendingStrings (unittest.TestCase):

    def setUp (self):
        self.lass = LengthAscendingStrings(['abc', 'bcd', 'a', 'abcd'])
        self.reordered = ['a', 'bcd', 'abc', 'abcd']

    def test__init__ (self):
        self.assertListEqual(self.lass, self.reordered)
        # Note: assertDictEqual does not differentiate dict and OrderedDict
        self.assertDictEqual(self.lass.lenbounds, {1:(0,1), 3:(1,3), 4:(3,4)})
        self.assertDictEqual(self.lass.lenbounds, {3:(1,3), 1:(0,1), 4:(3,4)})

    def test_isinstance (self):
        self.assertIsInstance(self.lass, LengthAscendingStrings)
        self.assertIsInstance(self.lass, TurboList)
        self.assertIsInstance(self.lass, list)

    def test__contains__ (self):
        self.assertTrue('abc' in self.lass)
        self.assertTrue('a' in self.lass)

    def test__len__ (self):
        self.assertTrue(len(self.lass)==4)

    def test__getitem__ (self):
        self.assertTrue(self.lass[3]=='abcd')
        self.assertListEqual(self.lass[:], self.reordered)
        self.assertListEqual(self.lass, self.reordered)
        self.assertListEqual(self.lass[1:2], ['bcd'])


if __name__ == '__main__':
    unittest.main()
