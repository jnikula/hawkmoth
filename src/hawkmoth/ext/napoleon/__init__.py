# Copyright (c) 2023, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from sphinx.ext import napoleon

def _process_docstring_proxy(app, lines, transform, options):
    if transform != app.config.hawkmoth_napoleon_transform:
        return

    # HACK: The Napoleon _process_docstring() function is for connecting to the
    # Sphinx autodoc autodoc-process-docstring event. It's ugly to call it
    # directly, but the alternative is duplicating all it does, which is also
    # ugly.

    return napoleon._process_docstring(app, None, None, None, options, lines)

def process_docstring(lines):
    """Simple interface for CLI and testing."""
    comment = '\n'.join(lines)
    config = napoleon.Config(napoleon_use_rtype=False)
    comment = str(napoleon.docstring.GoogleDocstring(comment, config))
    lines[:] = comment.splitlines()[:]

def setup(app):
    app.setup_extension('sphinx.ext.napoleon')
    app.setup_extension('hawkmoth')

    app.add_config_value('hawkmoth_napoleon_transform', 'napoleon', 'env', [str])

    app.connect('hawkmoth-process-docstring', _process_docstring_proxy)

    return {
        'parallel_read_safe': True,
    }
