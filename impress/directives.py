# -*- coding: utf-8 -*-
import os
import glob
import shutil
from impress import monkeys # NOQA
from impress import funcs
from docutils.parsers import rst
from docutils.parsers.rst import directives


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
            if item == '_modules':
                continue
            if os.path.isdir(join(item[1:])):
                shutil.rmtree(join(item[1:]))
            if item == '_static':
                for dirname in glob.glob(join(item, '*', '.git')):
                    shutil.rmtree(dirname)
            shutil.move(join(item), join(item[1:]))


def hide_title(argument):
    return directives.choice(argument, ('true', 'false'))


class Impress(rst.Directive):
    """This directive allow to set impress globales options"""
    required_arguments = 0
    optional_arguments = 4
    final_argument_whitespace = True
    has_content = False
    option_spec = {
                   'func': directives.unchanged,
                   'class': directives.class_option,
                   'hide-title': hide_title,
                   'data-scale': directives.nonnegative_int,
                  }

    opts = {}

    def run(self):
        if 'reset' in os.environ:
            Impress.opts = {}
        source = self.state.document.attributes['source']
        Impress.opts.setdefault(source, {}).update(self.options)
        return []


class Step(rst.Directive):
    """This directive allow to create some steps in rest documents"""
    amount = 0
    last_coord = {}

    required_arguments = 0
    optional_arguments = 5
    final_argument_whitespace = True
    has_content = False
    option_spec = {
                   'func': directives.unchanged,
                   'class': directives.class_option,
                   'hide-title': hide_title,
                   'data-scale': directives.nonnegative_int,
                   'data-x': directives.unchanged,
                   'data-y': directives.unchanged,
                   'data-z': directives.unchanged,
                   'data-rotate': directives.unchanged,
                   'data-rotate-x': directives.unchanged,
                   'data-rotate-y': directives.unchanged,
                   'data-rotate-z': directives.unchanged,
                   }

    def resolve_func(self, name):
        if hasattr(funcs, name):
            return getattr(funcs, name)
        else:
            mod, func = name.split('.')
            mod = __import__(mod, globals(), locals(), [''])
            return getattr(mod, func)

    def run(self):
        if 'reset' in os.environ:
            del os.environ['reset']
            Step.amounts = {}
            Step.last_coord = {}

        parent = self.state.parent
        source = parent.document.attributes['source']
        global_options = Impress.opts.setdefault(source, {})
        for k, v in global_options.items():
            if k not in self.options:
                self.options[k] = v

        if parent.starttag().startswith('<section'):
            attrs = self.state.parent.attributes
            attrs.update(self.options)
            if 'class' in self.options:
                attrs['classes'].extend(self.options.pop('class'))
            attrs['classes'].insert(0, 'step')
            if self.options.get('hide-title', 'false') == 'true':
                title = parent.next_node()
                title.attributes['classes'].insert(0, 'hidden')
            if 'data-x' not in self.options:
                func = self.resolve_func(self.options.get('func', 'default'))
                amount = Step.amounts.setdefault(source, 0)
                last_coord = Step.last_coord.setdefault(source, {})
                new_attrs = func(self, amount, last_coord)
                for k, v in new_attrs.items():
                    last_coord[k] = v
                    if k in ('x', 'y', 'z',
                             'rotate_x', 'rotate_y', 'rotate_z',
                             'scale'):
                        k = 'data-%s' % k.replace('_', '-')
                        if k not in self.options:
                            attrs[k] = [str(v)]
                Step.amounts[source] += 1
        else:
            print('%s:: WARNING: %s found out of section are ignored' % (
                             source, self.__class__.__name__.lower()))
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
    app.add_directive('impress', Impress)
    app.add_directive('step', Step)
    app.add_directive('slide', Slide)
    app.connect('html-page-context', change_pathto)
    app.connect('build-finished', move_private_folders)
