# -*- coding: utf-8 -*-
from sphinx.util import osutil
from docutils.writers.html4css1 import HTMLTranslator


def starttag(self, node, tagname, suffix='\n', empty=False, **attributes):
    attrs = node.non_default_attributes().items()
    attributes.update(dict([(k, v) for k, v in attrs
                           if k.startswith('data-')]))
    result = HTMLTranslator_starttag(self, node, tagname,
                                     suffix=suffix, empty=empty, **attributes)
    return result

HTMLTranslator_starttag = HTMLTranslator.starttag
HTMLTranslator.starttag = starttag


def relative_uri(base, to):
    if to.startswith('_'):
        to = to[1:]
    return osutil_relative_uri(base, to)

osutil_relative_uri = osutil.relative_uri
osutil.relative_uri = relative_uri
