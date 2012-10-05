# -*- coding: utf-8 -*-
from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils.writers.html4css1 import HTMLTranslator
import os
import shutil


def change_pathto(app, pagename, templatename, context, doctree):
    pathto = context.get('pathto')

    def gh_pathto(otheruri, *args, **kw):
        if otheruri.startswith('_'):
            otheruri = otheruri[1:]
        return pathto(otheruri, *args, **kw)
    context['pathto'] = gh_pathto


def move_private_folders(app, e):
    def join(dir, *args):
        return os.path.join(app.builder.outdir, dir, *args)

    for item in os.listdir(app.builder.outdir):
        if item.startswith('_') and os.path.isdir(join(item)):
            if os.path.isdir(join(item[1:])):
                shutil.rmtree(join(item[1:]))
            if item == '_static':
                shutil.rmtree(join(item, 'impress', 'impress', '.git'))
            shutil.move(join(item), join(item[1:]))


_old_starttag = HTMLTranslator.starttag


def starttag(self, node, tagname, suffix='\n', empty=False, **attributes):
    attrs = node.non_default_attributes().items()
    attributes.update(dict([(k, v) for k, v in attrs
                                        if k.startswith('data-')]))
    return _old_starttag(self, node, tagname,
                         suffix='\n', empty=False, **attributes)

HTMLTranslator.starttag = starttag


class Step(rst.Directive):
    """This directive allow to create some steps in rest documents"""
    amount = 0
    required_arguments = 0
    optional_arguments = 5
    final_argument_whitespace = True
    has_content = False
    option_spec = {'class': directives.class_option,
                   'data-x': directives.unchanged,
                   'data-y': directives.unchanged,
                   'data-scale': directives.unchanged,
                   'hide-title': directives.unchanged,
                   }

    def run(self):
        parent = self.state.parent
        if parent.starttag().startswith('<section'):
            attrs = self.state.parent.attributes
            attrs.update(self.options)
            if 'class' in self.options:
                attrs['classes'].extend(self.options.pop('class'))
            attrs['classes'].insert(0, 'step')
            if 'hide-title' in self.options:
                title = parent.next_node()
                title.attributes['classes'].insert(0, 'hidden')
            self.__class__.amount += 1
            if 'data-x' not in self.options:
                attrs['data-x'] = ['%s' % (1000 * self.__class__.amount)]
            if 'data-y' not in self.options:
                attrs['data-y'] = ['0']
        return []


class Slide(Step):
    """This directive allow to create some slides in rest documents"""

    def run(self):
        if 'class' in self.options:
            self.options['class'].append('slide')
        else:
            self.options['class'] = ['slide']
        return super(Slide, self).run()


def setup(app):
    app.add_directive('step', Step)
    app.add_directive('slide', Slide)
    app.connect('html-page-context', change_pathto)
    app.connect('build-finished', move_private_folders)
