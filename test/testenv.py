# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import sys
import os

testext = '.c'
testdir = os.path.dirname(os.path.abspath(__file__))
rootdir = os.path.dirname(testdir)

sys.path.insert(0, rootdir)

def get_testcases(path):
    for f in sorted(os.listdir(path)):
        if f.endswith(testext):
            yield os.path.join(path, f)

def get_testcase_options(testcase):
    options_filename = modify_filename(testcase, ext='stdin')

    # options are optional
    options = {}
    if os.path.isfile(options_filename):
        with open(options_filename, 'r') as file:
            for line in file.readlines():
                line = line.strip()
                # legacy
                if line.startswith('--'):
                    line = line[2:]

                opt = line.split('=', 1)
                options[opt[0]] = opt[1]

    return options

def modify_filename(filename, **kwargs):
    ext = kwargs.get('ext')
    if ext is not None:
        base, extension = os.path.splitext(filename)
        filename = base + '.' + ext

    dirname = kwargs.get('dir')
    if dirname is not None:
        base = os.path.basename(filename)
        filename = os.path.join(dirname, base)

    return filename

def read_file(filename, **kwargs):
    filename = modify_filename(filename, **kwargs)

    with open(filename, 'r') as file:
        expected = file.read()

    return expected
