# -*- coding: utf-8 -*-
import math

defaults = dict(x=0, y=0, rotate_x=0, rotate_y=0, rotate_z=0, scale=1)


def default(slide, slides):
    """:doc:`default`"""
    if slide.index > 0:
        slide.x += 1000
        slide.y += 500
        slide.rotate_x += (1000 / 180. * math.pi)


def linear(slide, slides):
    """:doc:`linear`"""
    if slide.index > 0:
        slide.x += 1000


def square(slide, slides):
    """:doc:`square`"""
    if slide.index % 4 == 3:
        slide.x = 0
        slide.y += 800
    else:
        slide.x += 1000


def spiral(slide, slides):
    """:doc:`spiral`"""
    r = 1200
    i = slide.index
    if i > 0:
        if slide.x > 0:
            incr = 100 * i / 3.
        else:
            incr = -100 * i / 3.
        slide.x = math.cos(i) * r
        slide.y = math.sin(i) * r
        slide.z = math.log(i) * r
        slide.rotate_x += ((r + incr) / 180. * math.pi)
        slide.rotate_y += ((r + incr) / 180. * math.pi)
        slide.rotate_y += ((r + incr) / 180. * math.pi)
