# SPDX-FileCopyrightText: 2026 Jani Nikula <jani@nikula.org>
# SPDX-License-Identifier: BSD-2-Clause

import ctypes

import sphinx
from clang import cindex


def _libclang_version():
    try:
        lib = cindex.conf.get_cindex_library()
        lib.clang_getClangVersion.restype = ctypes.c_char_p
        return lib.clang_getClangVersion().decode('utf-8')
    except Exception:
        return 'unknown'


def pytest_report_header(config):
    dependencies = [
        f'Sphinx {sphinx.__version__}',
        f'Clang {_libclang_version()}',
    ]

    return f'dependencies: {", ".join(dependencies)}'
