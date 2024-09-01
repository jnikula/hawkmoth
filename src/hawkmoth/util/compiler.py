# Copyright (c) 2021 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Compiler helpers
================

This module provides helper functions to access compiler information outside of
the Clang Python Bindings, for example system include paths.
"""

import subprocess

def _removesuffix(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    else:
        return s[:]

def _get_paths_from_output(output):
    started = False
    for line in output.splitlines():
        if not started:
            if line == '#include <...> search starts here:':
                started = True
            continue

        if line == 'End of search list.':
            break

        # Clang on macOS may print this.
        line = _removesuffix(line, '(framework directory)')

        yield line.strip()

def _get_include_paths(cc_path, lang):
    if lang == 'cpp':
        lang = 'c++'

    result = subprocess.run([cc_path, '-x', lang, '-E', '-Wp,-v', '-'],
                            stdin=subprocess.DEVNULL,
                            capture_output=True,
                            check=True,
                            text=True)

    return _get_paths_from_output(result.stderr)

def get_include_args(cc_path='clang', lang='c'):
    return [f'-I{path}' for path in _get_include_paths(cc_path=cc_path, lang=lang)]

if __name__ == '__main__':
    import argparse
    import os
    import pprint

    parser = argparse.ArgumentParser()
    parser.add_argument('cc_path', action='store', nargs='?', default='clang')
    parser.add_argument('--lang',
                        choices=[
                            'c',
                            'c++',
                            'cpp',
                        ], default='c')
    parser.add_argument('--output',
                        choices=[
                            'path',
                            'args',
                            'default',
                        ], default='default')

    args = parser.parse_args()

    if args.output == 'path':
        print(os.pathsep.join(_get_include_paths(cc_path=args.cc_path, lang=args.lang)))
    elif args.output == 'args':
        print('\n'.join(get_include_args(cc_path=args.cc_path, lang=args.lang)))
    else:
        pprint.pprint(get_include_args(cc_path=args.cc_path, lang=args.lang))
