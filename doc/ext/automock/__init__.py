# Copyright (c) 2020, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Automock
========

Sphinx C Domain directive extension to mock Hawkmoth by reading the
corresponding expected .rst test result instead of actual processing.
"""

import os

from docutils.parsers.rst import directives
from sphinx.directives.other import Include

class Automock(Include):
    required_argument = 1
    optional_arguments = 1

    # Allow passing a variable number of file patterns as arguments
    final_argument_whitespace = True

    option_spec = {
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
    app.add_config_value('cautodoc_root', app.confdir, 'env')
    app.add_config_value('cautodoc_compat', None, 'env')
    app.add_config_value('cautodoc_clang', None, 'env')
    app.add_directive_to_domain('c', 'autodoc', Automock)

    return dict(version = '0',
                parallel_read_safe = True, parallel_write_safe = True)
