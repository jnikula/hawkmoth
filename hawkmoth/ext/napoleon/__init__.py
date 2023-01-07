# Copyright (c) 2023, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from sphinx.ext.napoleon import _process_docstring

def _process_docstring_proxy(app, transform, options, lines):
    if transform is None or transform not in app.config.hawkmoth_napoleon_transform:
        return

    # The Napoleon _process_docstring() function is for connecting to the Sphinx
    # autodoc autodoc-process-docstring event. It's ugly to call it directly,
    # but the alternative is duplicating all it does, which is also ugly.

    return _process_docstring(app, None, None, None, options, lines)

def setup(app):
    app.setup_extension('sphinx.ext.napoleon')
    app.setup_extension('hawkmoth')

    app.add_config_value('hawkmoth_napoleon_transform', ['napoleon'], 'env', [list])

    app.connect('hawkmoth-process-docstring', _process_docstring_proxy)

    return {
        'parallel_read_safe': True,
    }
