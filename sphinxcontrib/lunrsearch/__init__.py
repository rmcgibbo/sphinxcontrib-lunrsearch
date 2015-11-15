import os
import itertools

from six import iteritems
import sphinx.search
from sphinx.util.osutil import copyfile
from sphinx.jinja2glue import SphinxFileSystemLoader
EXT_ROOT = os.path.dirname(__file__)


class IndexBuilder(sphinx.search.IndexBuilder):
    def freeze(self):
        """Create a usable data structure for serializing."""
        filenames, titles = zip(*sorted(self._titles.items()))
        fn2index = dict((f, i) for (i, f) in enumerate(filenames))

        objects = self.get_objects(fn2index)  # populates _objtypes
        objtypes = dict((v, k[0] + ':' + k[1])
                        for (k, v) in iteritems(self._objtypes))

        store = {}
        c = itertools.count()
        for prefix, items in iteritems(objects):
            for name, (index, typeindex, _, _) in iteritems(items):
                store[next(c)] = {
                    'filename': filenames[index],
                    'objtype': objtypes[typeindex],
                    'prefix': prefix,
                    'last_prefix': prefix.split('.')[-1],
                    'name': name,
                }

        return {'store': store}


def add_templates(app):
    app.builder.templates.loaders.insert(0, SphinxFileSystemLoader(EXT_ROOT))


def copy_static_files(app, exc):
    files = ['js/searchbox.js', 'css/searchbox.css']
    for f in files:
        abspath = os.path.join(EXT_ROOT, f)
        copyfile(abspath, os.path.join(app.outdir, '_static', f))


def setup(app):
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir

    app.add_javascript('js/searchbox.js')
    app.add_stylesheet('css/searchbox.css')
    app.add_javascript('https://cdnjs.cloudflare.com/ajax/libs/lunr.js/0.6.0/lunr.min.js')
    app.connect('builder-inited', add_templates)
    app.connect('build-finished', copy_static_files)

    sphinx.search.IndexBuilder = IndexBuilder
