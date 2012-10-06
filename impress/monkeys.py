# -*- coding: utf-8 -*-
from docutils.writers.html4css1 import HTMLTranslator

_old_starttag = HTMLTranslator.starttag


def starttag(self, node, tagname, suffix='\n', empty=False, **attributes):
    attrs = node.non_default_attributes().items()
    attributes.update(dict([(k, v) for k, v in attrs
                                        if k.startswith('data-')]))
    result = _old_starttag(self, node, tagname,
                         suffix='\n', empty=False, **attributes)
    return result

HTMLTranslator.starttag = starttag
