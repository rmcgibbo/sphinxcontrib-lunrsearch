import os
from os.path import dirname, join, exists
import json
import warnings
import itertools

from six import iteritems
import sphinx.search
from sphinx.util.osutil import copyfile
from sphinx.jinja2glue import SphinxFileSystemLoader


class IndexBuilder(sphinx.search.IndexBuilder):
    def freeze(self):
        """Create a usable data structure for serializing."""
        data = super(IndexBuilder, self).freeze()

        store = {}
        c = itertools.count()
        for prefix, items in iteritems(data['objects']):
            for name, (index, typeindex, _, shortanchor) in iteritems(items):
                objtype = data['objtypes'][typeindex]
                if objtype.startswith('cpp:'):
                    split =  name.rsplit('::', 1)
                    if len(split) != 2:
                        warnings.warn("What's up with %s?" % str((prefix, name, objtype)))
                        continue
                    prefix, name = split
                    last_prefix = prefix.split('::')[-1]
                else:
                    last_prefix = prefix.split('.')[-1]

                store[next(c)] = {
                    'filename': data['filenames'][index],
                    'objtype': objtype,
                    'prefix': prefix,
                    'last_prefix': last_prefix,
                    'name': name,
                    'shortanchor': shortanchor,
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
    app.builder.templates.loaders.insert(0, SphinxFileSystemLoader(dirname(__file__)))

    # adds the variable to the context used when rendering the searchbox.html
    app.config.html_context.update({
        'lunrsearch_highlight': json.dumps(bool(app.config.lunrsearch_highlight))
    })


def copy_static_files(app, _):
    # because we're using the extension system instead of the theme system,
    # it's our responsibility to copy over static files outselves.
    files = ['js/searchbox.js', 'css/searchbox.css']
    for f in files:
        src = join(dirname(__file__), f)
        dest = join(app.outdir, '_static', f)
        if not exists(dirname(dest)):
            os.makedirs(dirname(dest))
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
