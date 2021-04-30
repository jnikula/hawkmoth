# Copyright (c) 2016-2019 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Hawkmoth parser debug tool
==========================

python3 -m hawkmoth
"""

import argparse
import sys

from hawkmoth.parser import parse
from hawkmoth.util import doccompat

def main():
    parser = argparse.ArgumentParser(prog='hawkmoth', description="""
    Hawkmoth parser debug tool. Print the documentation comments extracted
    from FILE, along with the generated C Domain directives, to standard
    output. Include metadata with verbose output.""")
    parser.add_argument('file', metavar='FILE', type=str, action='store',
                        help='The C source or header file to parse.')
    parser.add_argument('--compat',
                        choices=['none',
                                 'javadoc-basic',
                                 'javadoc-liberal',
                                 'kernel-doc'],
                        help='Compatibility options. See cautodoc_compat.')
    parser.add_argument('--clang', metavar='PARAM', action='append',
                        help='Argument to pass to Clang. May be specified multiple times. See cautodoc_clang.')
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='Verbose output.')
    args = parser.parse_args()

    transform = lambda comment: doccompat.convert(comment, transform=args.compat)

    docs, errors = parse(args.file, transform=transform, clang=args.clang)

    for (doc, meta) in docs:
        if args.verbose:
            print(f'# {meta}')
        print(doc)

    for (severity, filename, lineno, msg) in errors:
        if filename:
            print('f{severity.name}: {filename}:{lineno}: {msg}',
                  file=sys.stderr)
        else:
            print(f'{severity.name}: {msg}', file=sys.stderr)

main()
