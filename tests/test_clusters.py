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
print('Executing %s' %  __file__)

import unittest

from containers import TurboList, Clusters


class Test_Clusters (unittest.TestCase):

    def setUp (self):
        objects = TurboList ([-9, 'a', (1,2), 222])
        self.clusters = Clusters (objects)

    def test__init__ (self):
        clusters = self.clusters
        self.assertEqual(len(clusters), 0)
        self.assertEqual(len(clusters._cids), 4)

    def test_merge_1 (self):

        #objects = TurboList ([-9, 'a', (1,2), 222])
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

        #objects = TurboList ([-9, 'a', (1,2), 222])
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
