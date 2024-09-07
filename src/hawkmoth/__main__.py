# Copyright (c) 2016-2019 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Hawkmoth parser debug tool
==========================

python3 -m hawkmoth
"""

import argparse
import os
import sys

from hawkmoth.ext import javadoc
from hawkmoth.ext import napoleon
from hawkmoth.parser import parse

def filename(file):
    if os.path.isfile(file):
        return file
    raise ValueError

def _process_docstring(transform, lines):
    transformations = {
        'napoleon': napoleon.process_docstring,
        'javadoc': javadoc.process_docstring,
    }

    fn = transformations.get(transform)
    if fn:
        fn(lines)

def _read_version():
    try:
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               'VERSION')) as version_file:
            version = version_file.read().strip()
    except OSError:
        version = '(unknown version)'

    return version

def main():
    parser = argparse.ArgumentParser(prog='hawkmoth', description="""
    Hawkmoth parser debug tool. Print the documentation comments extracted
    from FILE, along with the generated C Domain directives, to standard
    output. Include metadata with verbose output.""")
    parser.add_argument('file', metavar='FILE', type=filename, action='store',
                        help='The C or C++ source or header file to parse.')
    parser.add_argument('--domain',
                        choices=['c', 'cpp'],
                        default='c',
                        help='Sphinx domain to be used.')
    compat = parser.add_mutually_exclusive_group()
    compat.add_argument('--process-docstring',
                        choices=[
                            'javadoc',
                            'napoleon',
                        ],
                        help='Process docstring.')
    parser.add_argument('--clang', metavar='PARAM', action='append',
                        help='Argument to pass to Clang. May be specified multiple times. See hawkmoth_clang.')  # noqa: E501
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='Verbose output.')
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s {_read_version()}',
                        help='Show version and exit')
    args = parser.parse_args()

    comments, errors = parse(args.file, domain=args.domain, clang_args=args.clang)

    if args.process_docstring:
        def process_docstring(lines): return _process_docstring(args.process_docstring, lines)
    else:
        process_docstring = None

    for comment in comments.walk():
        if args.verbose:
            print(f'# {comment.get_meta()}')
        lines, _ = comment.get_docstring(process_docstring=process_docstring)
        print('\n'.join(lines))

    for error in errors:
        print(f'{error.level.name}: {error.get_message()}', file=sys.stderr)

if __name__ == '__main__':
    main()
