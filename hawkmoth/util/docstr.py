# Copyright (c) 2016-2020 Jani Nikula <jani@nikula.org>
# Copyright (c) 2018-2020 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Documentation strings manipulation library
==========================================

This module allows a generic way of generating reST documentation for each C
construct.
"""

import re

def is_doc(comment):
    """Test if comment is a C documentation comment."""
    return comment.startswith('/**') and comment != '/**/'
