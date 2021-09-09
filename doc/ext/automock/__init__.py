# Copyright (c) 2020, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Automock
========

Sphinx C Domain directive extension to mock Hawkmoth by reading the
corresponding expected .rst test result instead of actual processing.

This is not an example how to do documentation fallbacks for regular projects
when Hawkmoth is not available.
"""

import os

from docutils.parsers.rst import directives
from sphinx.directives.other import Include

class Automock(Include):
    required_arguments = 1
    optional_arguments = 100 # arbitrary limit

    option_spec = {
        'transform': directives.unchanged_required,
        'compat': directives.unchanged_required,
        'clang': directives.unchanged_required,
    }
    has_content = False

    def run(self):
        # Use include directive implementation with .c -> .rst
        base, extension = os.path.splitext(self.arguments[0])
        self.arguments[0] = base + '.rst'

        return super(Include, self).run()

def setup(app):
    app.add_config_value('cautodoc_root', app.confdir, 'env', [str])
    app.add_config_value('cautodoc_compat', None, 'env', [str])
    app.add_config_value('cautodoc_transformations', None, 'env', [dict])
    app.add_config_value('cautodoc_clang', [], 'env', [list])
    app.add_directive_to_domain('c', 'autodoc', Automock)

    return dict(version = '0',
                parallel_read_safe = True, parallel_write_safe = True)
