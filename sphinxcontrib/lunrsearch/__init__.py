import os
import json
import itertools

from six import iteritems
import sphinx.search
from sphinx.util.osutil import copyfile
from sphinx.jinja2glue import SphinxFileSystemLoader
EXT_ROOT = os.path.dirname(__file__)


class IndexBuilder(sphinx.search.IndexBuilder):
    def freeze(self):
        """Create a usable data structure for serializing."""
        data = super(IndexBuilder, self).freeze()

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

        data.update({'store': store})
        return data


def builder_inited(app):
    # adding a new loader to the template system puts our searchbox.html
    # template in front of the others, it overrides whatever searchbox.html
    # the current theme is using.
    # it's still up to the theme to actually _use_ a file called searchbox.html
    # somewhere in its layout. but the base theme and pretty much everything
    # else that inherits from it uses this filename.
    app.builder.templates.loaders.insert(0, SphinxFileSystemLoader(EXT_ROOT))

    # adds the variable to the context used when rendering the searchbox.html
    app.config.html_context.update({
        'lunrsearch_highlight': json.dumps(bool(app.config.lunrsearch_highlight))
    })

def copy_static_files(app, exc):
    # because we're using the extension system instead of the theme system,
    # it's our responsibility to copy over static files outselves.
    files = ['js/searchbox.js', 'css/searchbox.css']
    for f in files:
        src = os.path.join(EXT_ROOT, f)
        dest = os.path.join(app.outdir, '_static', f)
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        copyfile(src, dest)


def setup(app):
    # adds <script> and <link> to each of the generated pages to load these
    # files.
    app.add_javascript('https://cdnjs.cloudflare.com/ajax/libs/lunr.js/0.6.0/lunr.min.js')
    app.add_stylesheet('css/searchbox.css')
    app.add_javascript('js/searchbox.js')


    app.connect('builder-inited', builder_inited)
    app.connect('build-finished', copy_static_files)
    app.add_config_value('lunrsearch_highlight', True, 'html')

    sphinx.search.IndexBuilder = IndexBuilder
