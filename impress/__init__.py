from optparse import OptionParser
from impress import ghp
import subprocess as sp
import tempfile
import sphinx
import sys
import os


def build_pages(git=False):
    d = tempfile.mkdtemp(prefix='impress-')
    print('Building doc in %s...' % d)
    cmd = (
        'rm -Rf %(d)s; mkdir -p %(d)s;'
        '%(b)s -i $(find . -name index.rst) -o %(d)s;'
        "find %(d)s -name '*html' -exec sed 's/_images/static/g' -i {} \\;"
    ) % dict(d=d, b=os.path.abspath(sys.argv[0]))
    print(cmd)
    sp.check_call(cmd, shell=True)
    if git:
        if not ghp.try_rebase('origin', 'gh-pages'):
            print("Failed to rebase gh-pages branch.")
            return
        ghp.run_import(d, 'gh-pages', 'Update documentation',
                       nojekyll=False)
        sp.check_call(['git', 'push', 'origin', 'gh-pages'])


def main():
    parser = OptionParser()
    parser.usage = '''%prog -i filename.rst [-o outputdir]'''
    parser.add_option('-i', '--input', metavar="FILENAME",
                      dest='input', default='index.rst',
                      help="Input file. Default to: index.rst")
    parser.add_option('-o', '--output', metavar="DIRNAME",
                      dest='output', default='html',
                      help="Output dir. Default to: html")
    parser.add_option('-l', '--loop', metavar='DELAY',
                      dest='loop', default=None,
                      help="Loop over the command each DELAY second")
    parser.add_option('-b', '--build', action="store_true",
                      dest='build', default=False,
                      help="Build slides in pages/")
    parser.add_option('-g', '--github', action="store_true",
                      dest='build_gh', default=False,
                      help="Build slides and push the result to gh-pages")
    options, args = parser.parse_args()

    if options.build:
        build_pages(git=False)
        return
    elif options.build_gh:
        build_pages(git=True)
        return

    options.output = os.path.abspath(options.output)

    if options.loop:
        try:
            float(options.loop)
        except:
            parser.error('Invalid loop option')

    if not os.path.isfile(options.input):
        parser.error((
            '%s does not exist. Use a correct reST file with as input'
        ) % options.input)

    filename = options.input
    docdir = os.path.dirname(filename) or os.getcwd()
    sys.path.insert(0, os.path.abspath(docdir))

    master_doc, ext = os.path.splitext(os.path.basename(filename))
    os.environ['master_doc'] = master_doc
    os.environ['source_suffix'] = ext
    os.environ['exclude_patterns'] = options.output

    sys.argv[1:] = [
        '-q', '-b', 'html',
        '-c', os.path.dirname(__file__),
        '-d', os.path.join(options.output, 'doctrees'),
    ]
    sys.argv.extend([
        '.',
        options.output] + args)
    os.chdir(docdir)
    if os.path.isdir('static'):
        os.environ['html_static_path'] = os.path.abspath('static')
    if os.path.isdir('templates'):
        os.environ['templates_path'] = os.path.abspath('templates')
    os.environ['reset'] = '1'
    if options.loop:
        import time
        argv = sys.argv[:]
        argv.insert(1, '-a')
        argv.insert(1, '-E')
        env = os.environ.copy()
        while True:
            try:
                os.environ.update(env)
                sphinx.main(argv)
                time.sleep(float(options.loop))
            except KeyboardInterrupt:
                break
    else:
        sys.exit(sphinx.main())
