

def main():
    from optparse import OptionParser
    import sphinx
    import sys
    import os

    parser = OptionParser()
    parser.usage = '''%prog -i filename.rst [-o outputdir]'''
    parser.add_option('-i', dest='input', default='index.rst',
                      help="Input file. Default to: index.rst")
    parser.add_option('-o', dest='output', default='html',
                      help="Output dir. Default to: html")
    options, args = parser.parse_args()

    options.output = os.path.abspath(options.output)

    if not os.path.isfile(options.input):
        parser.error((
            '%s does not exist. Use a correct reST file with as input'
           ) % options.input)

    filename = options.input
    docdir = os.path.dirname(filename)

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
        os.environ['html_static_path'] = 'static'
    sys.exit(sphinx.main())
