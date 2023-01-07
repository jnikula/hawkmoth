# Copyright (c) 2023, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from hawkmoth.util.doccompat import javadoc_liberal

def _process_docstring(app, lines, transform, options):
    if transform != app.config.hawkmoth_javadoc_transform:
        return

    comment = '\n'.join(lines)
    comment = javadoc_liberal(comment)
    lines[:] = comment.splitlines()[:]

def setup(app):
    app.setup_extension('hawkmoth')

    app.add_config_value('hawkmoth_javadoc_transform', 'javadoc', 'env', [str])

    app.connect('hawkmoth-process-docstring', _process_docstring)

    return {
        'parallel_read_safe': True,
    }
