#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import shutil
import unittest

import testenv
from sphinx_testing import with_app

@with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='text')
def _get_output(input_filename, app, status, warning, **options):
    shutil.copyfile(input_filename,
                    testenv.modify_filename(input_filename, dir=app.srcdir))

    with open(os.path.join(app.srcdir, 'index.rst'), 'w') as f:
        fmt = '.. c:autodoc:: {source}\n'
        f.write(fmt.format(source=os.path.basename(input_filename)))
        for key in [k for k in options.keys() if k in testenv.directive_options]:
            fmt = '   :{key}: {value}\n'
            f.write(fmt.format(key=key, value=options[key]))

    app.build()

    return testenv.read_file(os.path.join(app.outdir, 'index.txt')), None

@with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='text')
def _get_expected(input_filename, app, status, warning, **options):
    shutil.copyfile(testenv.modify_filename(input_filename, ext='rst'),
                    os.path.join(app.srcdir, 'index.rst'))

    app.build()

    return testenv.read_file(os.path.join(app.outdir, 'index.txt')), None

class DirectiveTest(unittest.TestCase):
    pass

testenv.assign_test_methods(DirectiveTest, _get_output, _get_expected)

if __name__ == '__main__':
    unittest.main()
