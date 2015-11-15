sphinxcontrib-lunrsearch
========================

This extension modifies the search box in Sphinx documentation
to show instant results as you type. It's particularly suited for
searching through APIs.

To use, add ``'sphinxcontrib.lunrsearch'`` to the list of extensions in your
sphinx ``conf.py`` file.

Options
-------

The following options can be set in conf.py:

- lunrsearch_highlight: bool

  Whether to highlight the seach term after navigating to a results.
  The default is ``False``.
