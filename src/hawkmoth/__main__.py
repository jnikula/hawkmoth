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

from hawkmoth.parser import parse
from hawkmoth.util import doccompat

def filename(file):
    if os.path.isfile(file):
        return file
    raise ValueError

def transform(args, lines):
    text = '\n'.join(lines)
    text = doccompat.convert(text, transform=args.compat)
    lines[:] = [line for line in text.splitlines()]

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
    parser.add_argument('--compat',
                        choices=['none',
                                 'javadoc-basic',
                                 'javadoc-liberal',
                                 'kernel-doc'],
                        help='Compatibility options. See cautodoc_compat.')
    parser.add_argument('--clang', metavar='PARAM', action='append',
                        help='Argument to pass to Clang. May be specified multiple times. See cautodoc_clang.')  # noqa: E501
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='Verbose output.')
    args = parser.parse_args()

    comments, errors = parse(args.file, clang_args=args.clang)
    comments, errors = parse(args.file, domain=args.domain, clang_args=args.clang)

    for comment in comments.walk():
        if args.verbose:
            print(f'# {comment.get_meta()}')
        print('\n'.join(comment.get_docstring(transform=lambda lines: transform(args, lines))))

    for error in errors:
        print(f'{error.level.name}: {error.get_message()}', file=sys.stderr)

if __name__ == '__main__':
    main()
