#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import shutil

import pytest
from sphinx_testing import with_app

from test import testenv

@with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='text')
def _get_output(input_filename, app, status, warning, **options):
    shutil.copyfile(input_filename,
                    testenv.modify_filename(input_filename, dir=app.srcdir))

    with open(os.path.join(app.srcdir, 'index.rst'), 'w') as f:
        source = os.path.basename(input_filename)
        f.write(f'.. c:autodoc:: {source}\n')
        for key in [k for k in options.keys() if k in testenv.directive_options]:
            f.write(f'   :{key}: {options[key]}\n')

    app.build()

    return testenv.read_file(os.path.join(app.outdir, 'index.txt')), None

@with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='text')
def _get_expected(input_filename, app, status, warning, **options):
    shutil.copyfile(testenv.modify_filename(input_filename, ext='rst'),
                    os.path.join(app.srcdir, 'index.rst'))

    app.build()

    return testenv.read_file(os.path.join(app.outdir, 'index.txt')), None

@pytest.mark.parametrize('input_filename', testenv.get_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_directive(input_filename):
    testenv.run_test(input_filename, _get_output, _get_expected)
