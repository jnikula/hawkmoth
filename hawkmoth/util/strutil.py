# Copyright (c) 2021, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

def args_as_list(args):
    if isinstance(args, str):
        args = [s.strip() for s in args.split(',') if len(s.strip()) > 0]
    if args is None:
        args = []
    return args
