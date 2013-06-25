#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 04/20/2013, updated 06/25/2013
#
""" Unit tests
"""
print('Executing %s' %  __file__)

import unittest
import os, sys, time

import unittest

import poost.containers as containers


class Test_Clusters (unittest.TestCase):

    def setUp (self):
        objects = containers.TurboList ([-9, 'a', (1,2), 222])
        self.clusters = containers.Clusters (objects)

    def test__init__ (self):
        clusters = self.clusters
        self.assertEqual(len(clusters), 0)
        self.assertEqual(len(clusters._cids), 4)

    def test_merge_1 (self):

        #objects = containers.TurboList ([-9, 'a', (1,2), 222])
        clusters = self.clusters
        clusters.merge(-9, (1,2))
        self.assertListEqual(clusters._cids, [0, None, 0, None])
        self.assertEqual(len(clusters), 1)
        self.assertSetEqual(clusters[0], set([-9, (1,2)]))
        self.assertListEqual(clusters.unclustered, ['a', 222])

        clusters.merge('a', (1,2))
        self.assertListEqual(clusters._cids, [0, 0, 0, None])
        self.assertEqual(len(clusters), 1)
        self.assertSetEqual(clusters[0], set([-9, 'a', (1,2)]))
        self.assertListEqual(clusters.unclustered, [222])

        clusters.merge('a', 222)
        self.assertListEqual(clusters._cids, [0, 0, 0, 0])
        self.assertEqual(len(clusters), 1)
        self.assertSetEqual(clusters[0], set([-9, 'a', (1,2), 222]))
        self.assertListEqual(clusters.unclustered, [])

    def test_merge_2 (self):

        #objects = containers.TurboList ([-9, 'a', (1,2), 222])
        clusters = self.clusters
        clusters.merge(-9, (1,2))
        self.assertListEqual(clusters._cids, [0, None, 0, None])
        self.assertListEqual(clusters.unclustered, ['a', 222])

        clusters.merge('a', 222)
        self.assertListEqual(clusters._cids, [0, 1, 0, 1])
        self.assertEqual(len(clusters), 2)
        self.assertSetEqual(clusters[0], set([-9, (1,2)]))
        self.assertSetEqual(clusters[1], set(['a', 222]))
        self.assertListEqual(clusters.unclustered, [])

        clusters.merge('a', (1,2))
        self.assertListEqual(clusters._cids, [1, 1, 1, 1])
        self.assertEqual(len(clusters), 1)
        self.assertSetEqual(clusters[1], set([-9, 'a', (1,2), 222]))
        self.assertListEqual(clusters.unclustered, [])


if __name__ == '__main__':
    unittest.main()
