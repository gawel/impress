# -*- coding: utf-8 -*-
import os
import impress
extensions = [
        'impress.directives',
        'sphinx.ext.autodoc',
        'sphinx.ext.viewcode',
     ]
templates_path = ['templates']
source_suffix = os.environ['source_suffix']
master_doc = os.environ.pop('master_doc')
exclude_patterns = [os.environ.pop('exclude_patterns')]
pygments_style = 'sphinx'
html_theme = 'impress'
html_theme_path = [os.path.dirname(os.path.dirname(impress.__file__))]
html_static_path = []
if 'html_static_path' in os.environ:
    html_static_path = [os.environ.pop('html_static_path')]
