# -*- coding: utf-8 -*-
import math


class Slide(object):
    """Node wrapper to easyly set positioning"""

    def __init__(self, i, section):
        self.section = section
        self.attributes = section.attributes
        self.index = i

    @property
    def id(self):
        ids = self.section.attributes['dupnames']
        if ids:
            return ids[0]
        return self.section.attributes['ids'][0]

    def update(self, *others, **kwargs):
        attributes = {}
        for other in others:
            attributes.update(other.attributes)
        attributes.update(kwargs)
        for k, v in attributes.items():
            if k.startswith('data-') or k in ('func',):
                if k not in self.attributes:
                    if k not in ('data-scale',):
                        self.attributes[k] = v

    def __getattr__(self, attr):
        attr = attr.replace('_', '-')
        attr = 'data-%s' % attr
        default = attr == 'data-scale' and 1 or 0
        value = self.attributes.setdefault(attr, default)
        if isinstance(value, unicode):
            value = float(value)
        return value

    def __setattr__(self, attr, value):
        if attr in ('index', 'section', 'attributes'):
            object.__setattr__(self, attr, value)
        else:
            attr = attr.replace('_', '-')
            attr = 'data-%s' % attr
            self.section.attributes[attr] = value

    def __repr__(self):
        coord = ['%s: %s' % (k[5:], v) for k, v in self.attributes.items()
                                                  if k.startswith('data-')]
        coord = ', '.join(sorted(coord))
        classes = '.'.join(self.attributes.get('classes'))
        return '<slide#%s.%s (%i) {%s}>' % (self.id, classes,
                                            self.index, coord)


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


def square(slide, slides, amount=4):
    """:doc:`square`"""
    if not slide.index % amount and slide.index:
        slide.x = 0
        slide.y += 800
    else:
        slide.x += 1000


def square2(slide, slides, amount=4):
    """:doc:`square2`"""
    if slide.index == 0 or slide.incr_x == 0:
        slide.incr_x = 1000
    if not slide.index % amount and slide.index:
        slide.incr_x = -slide.incr_x
        slide.rotate_z = slide.rotate_z == 0 and 180 or 0
        slide.y += 800
    else:
        slide.x += slide.incr_x


def spiral(slide, slides, r=1200):
    """:doc:`spiral`"""
    i = slide.index
    if i > 0:
        slide.x = math.cos(i) * r
        slide.y = math.sin(i) * r
        slide.z = math.log(i) * r
        slide.rotate_x += (r / 180. * math.pi)
        slide.rotate_y += (r / 180. * math.pi)
        slide.rotate_y += (r / 180. * math.pi)
