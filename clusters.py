#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# CONTRIBUTORS (sorted by surname)
# LUO, Pengkui <pengkui.luo@gmail.com>
#
#
# UPDATED ON
# 2013: 04/20, 04/21, 05/30, 06/11, 07/29
#
"""

"""
__all__ = [
    'Cluster',
    'Clusters',
]
print('Executing %s' %  __file__)

from .turbolist import TurboList

class Cluster (set):
    """ The containter for a cluster.

        It is up to the caller to change every property.

        Warning: users should not assume this is a set type - may change later
    """
    def __init__ (self, objects, **kwargs):
        """ Constructor
        """
        set.__init__(self, objects)
        self.properties = {}

    def extend (self, objects):
        """ Adds multiple objects to the current cluster.
        """
        for obj in objects:
            set.add(self, obj)


class Clusters (dict):
    """ A generic container for storing clustering info for a TurboList object.

        Main data structor: subclassed from dict,
        mapping a cluster id [int] to an (initially empty) set of objects,
        where the object can be any arbitrary complex object.

        Usage:
        ------
        len(self): returns the number of formed clusters, initially 0.

        Other properties:
        -----------------
        'raw': [TurboList instance] original input objects - never changes
        '_cids': [list] of cluster ids, initially all None.
        'unclustered': [TurboList instance] not-yet-clustered objects.

    """

    def __init__ (self, objects, **kwargs):
        """ Constructor. Take a TurboList object as input.
        """
        assert isinstance(objects, TurboList)
        dict.__init__(self, {})
        self.raw = objects
        self.unclustered = TurboList(objects)
        self._cids = [None for _ in xrange(len(objects))]

    def get_all_clusters (self):
        """ Returns a list of all clusters.
        """
        return self.values()

    def create_cluster (self, objects):
        """ Create a cluster using a subset of objects.
        """
        assert set(objects).issubset(self.raw)
        cid0 = 1 + max([-1]+self.keys())
        self[cid0] = Cluster(objects)
        for obj in objects:
            i = self.raw.index(obj)
            self._cids[i] = cid0
            self.unclustered.remove(obj)

    def merge (self, obj1, obj2, *args):
        """  Merges belonging clusters of objects obj1, obj2, ... into one.
             returns the resulting cid0.
        """
        # Turbolist positions
        i1 = self.raw.index(obj1)
        i2 = self.raw.index(obj2)
        # Cluster IDs
        cid1 = self._cids[i1]
        cid2 = self._cids[i2]
        #cid0 = None

        # Case 1: neither obj1 nor obj2 has been clustered yet.
        if (cid1 is None) and (cid2 is None):
            cid0 = 1 + max([-1]+self.keys())  # in case len(self)==0
            self[cid0] = Cluster([obj1, obj2])
            self._cids[i1] = cid0
            self._cids[i2] = cid0
            self.unclustered.remove(obj1)
            self.unclustered.remove(obj2)

        # Case 2: obj1 was clustered into c1, but obj2 has not been clustered yet.
        elif (cid1 is not None) and (cid2 is None):
            self[cid1].add(obj2)
            cid0 = cid1
            self._cids[i2] = cid1
            self.unclustered.remove(obj2)

        # Case 3: s2 was clustered into c2, but s1 has not been clustered yet.
        elif (cid1 is None) and (cid2 is not None):
            self[cid2].add(obj1)
            cid0 = cid2
            self._cids[i1] = cid2
            self.unclustered.remove(obj1)

        # Case 4: both obj1 and obj2 have been clustered -> merge 2 clusters
        elif cid1 != cid2:  # if not in the same cluster already
            # merge the smaller cluster cid9 into the bigger one cid0
            if len(self[cid1]) >= len(self[cid2]):
                cid0, cid9 = cid1, cid2
            else:
                cid0, cid9 = cid2, cid1

            self[cid0].extend(self[cid9])
            for obj in self[cid9]:
                i = self.raw.index(obj)
                self._cids[i] = cid0
            del self[cid9]

            #cid0 = max(cid1, cid2)
            #set0 = self[cid1].union(self[cid2])
            #del self[cid1]
            #del self[cid2]
            #self[cid0] = set0
            #for obj in set0:
            #    i = self.raw.index(obj)
            #    self._cids[i] = cid0

        # Case 5: obj1 and obj2 were in the same cluster -> do nothing
        else: cid0 = cid1

        return cid0


    def delete_cluster (self, cid=None, obj=None):
        """ Delete a cluster either by cid, or through a member obj.
            obj, if available, will override cid.
        """
        if obj is not None:
            i = self.raw.index(obj)
            cid = self._cids[i]
        assert cid is not None
        cluster = self[cid]
        for cobj in cluster:
            self.unclustered.append(cobj)
            i = self.raw.index(cobj)
            self._cids[i] = None
        del self[cid]

    def purge_small_clusters (self, smallest_size=3):
        """ Purge clusters with size less than smallest_size.
        """
        # To prevent "dict changed size during iteration",
        # self.items() returns a copy
        for cid, cluster in self.items():
            if len(cluster) < smallest_size:
                self.delete_cluster(cid=cid)

    def indices_in_same_cluster (self, i1, i2, *args):
        """ True if objects with indices i1, i2, ... are in the same cluster.
        """
        return self._cids[i1] == self._cids[i2] >= 0

    def objects_in_same_cluster (self, obj1, obj2, *args):
        """ Returns True if objtects obj1, objt2, ... are in the same cluster.
        """
        i1 = self.raw.index(obj1)
        i2 = self.raw.index(obj2)
        return self.indices_in_same_cluster(i1, i2)


if __name__ == '__main__':

    def test_Cluster():
        c1 = Cluster([1, 2, 3])
        c1.properties['a'] = 'a1'
        c2 = Cluster([2, 3, 4])
        c2.properties['a'] = 'a2'


