#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2013 Pengkui Luo <pengkui.luo@gmail.com>
# Created 04/20/2013, updated 06/22/2013
#
# -- CONTRIBUTORS
# Hesham Mekky <hesham.zakareya@gmail.com>
#
""" nameddict variants.
"""
__all__ = [
    'NamedDict',
    'makestruct',
]
print('Executing %s' %  __file__)

import textwrap
from collections import OrderedDict


class NamedDict (OrderedDict):
    """ NamedDict
    """
    def __init__(self, attribute=None, **kwargs):
        indict = kwargs.items()
        self.attribute = attribute
        OrderedDict.__init__(self, indict)
        self.__initialised = True

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        if not self.__dict__.has_key('_NamedDict__initialised'):
            return OrderedDict.__setattr__(self, item, value)
        elif self.__dict__.has_key(item):
            OrderedDict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

    def __delattr__(self, item):
        if self.__dict__.has_key(item):
            OrderedDict.__delattr__(self, item)
        else:
            self.__delitem__(item)


def makestruct (name, fields):
    """
    http://stackoverflow.com/questions/2646157/what-is-the-fastest-to-access-struct-like-object-in-python
    """
    fields = fields.split()
    template = textwrap.dedent("""\
    class {name}(object):
        __slots__ = {fields!r}
        def __init__(self, {args}):
            {self_fields} = {args}
        def __getitem__(self, idx):
            return getattr(self, fields[idx])
    """).format(
        name=name,
        fields=fields,
        args=','.join(fields),
        self_fields=','.join('self.' + f for f in fields)
    )
    d = {'fields': fields}
    exec template in d
    return d[name]

