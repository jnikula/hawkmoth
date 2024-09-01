# Copyright (c) 2024, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from hawkmoth.util import compiler

clang_include_args = []

def pytest_addoption(parser):
    parser.addoption('--cc-path', action='store', default='clang')

def pytest_configure(config):
    global clang_include_args

    cc_path = config.getoption('--cc-path')

    clang_include_args = compiler.get_include_args(cc_path=cc_path)
