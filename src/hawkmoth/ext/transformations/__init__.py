# Copyright (c) 2023, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from sphinx.util import logging

def _process_docstring(app, lines, transform, options):
    transformations = app.config.cautodoc_transformations
    tropt = options.get('transform')

    if transformations is None:
        return

    # Note: None is a valid key for default.
    if tropt not in transformations:
        return

    # Note: None is a valid value for no transformation.
    transform = transformations.get(tropt)
    if transform is None:
        return

    comment = '\n'.join(lines)
    comment = transform(comment)
    lines[:] = comment.splitlines()[:]

def setup(app):
    logger = logging.getLogger(__name__)
    logger.warning('hawkmoth.ext.transformations extension has been deprecated.')

    app.add_config_value('cautodoc_transformations', None, 'env', [dict])

    # Run before event handlers with default priority.
    app.connect('hawkmoth-process-docstring', _process_docstring, 400)

    return {
        'parallel_read_safe': True,
    }
