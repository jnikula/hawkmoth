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
    parser.add_argument('--clang', metavar='PARAM[,PARAM,...]',
                        help='Arguments to pass to clang. See cautodoc_clang.')
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='Verbose output.')
    args = parser.parse_args()

    docs, errors = parse(args.file, compat=args.compat, clang=args.clang)

    for (doc, meta) in docs:
        if args.verbose:
            print('# {}'.format(meta))
        print(doc)

    for (severity, filename, lineno, msg) in errors:
        print('{}: {}:{}: {}'.format(severity.name,
                                     filename, lineno, msg), file=sys.stderr)

main()
