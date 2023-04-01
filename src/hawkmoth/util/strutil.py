# Copyright (c) 2021, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

def string_list(argument):
    if argument is None:
        return []

    return [s.strip() for s in argument.split(',') if len(s.strip()) > 0]
