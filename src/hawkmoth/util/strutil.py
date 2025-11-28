# SPDX-FileCopyrightText: 2021 Jani Nikula <jani@nikula.org>
# SPDX-License-Identifier: BSD-2-Clause


def string_list(argument):
    if argument is None:
        return []

    return [s.strip() for s in argument.split(",") if len(s.strip()) > 0]
