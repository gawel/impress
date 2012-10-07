# -*- coding: utf-8 -*-
import math

defaults = dict(x=0, y=0, rotate_x=0, rotate_y=0, rotate_z=0, scale=1)


def default(slide, i, coord, slides):
    """:doc:`default`"""
    if i > 0:
        coord['x'] += 1000
        coord['y'] += 500
        coord['rotate_x'] += (1000 / 180. * math.pi)
    return coord


def linear(slide, i, coord, slides):
    """:doc:`linear`"""
    if i > 0:
        coord['x'] += 1000
    return coord


def spiral(slide, i, coord, slides):
    """:doc:`spiral`"""
    r = 1200
    if i > 0:
        if coord['x'] > 0:
            incr = 100 * i / 3.
        else:
            incr = -100 * i / 3.
        coord['x'] = math.cos(i) * r
        coord['y'] = math.sin(i) * r
        coord['z'] = math.log(i) * r
        coord['rotate_x'] += ((r + incr) / 180. * math.pi)
        coord['rotate_y'] += ((r + incr) / 180. * math.pi)
        coord['rotate_y'] += ((r + incr) / 180. * math.pi)
    return coord
