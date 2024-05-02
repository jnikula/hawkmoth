#!/bin/bash
# Copyright (c) 2023, Jani Nikula <jani@nikula.org>
# SPDX-License-Identifier: BSD-2-Clause

# Output a json matrix for building multiple versions of documentation

# Can't use git describe unless full history has been fetched!
release=$(git tag --list --sort=version:refname | tail -1)

jq -c . <<EOF
{
  "include": [
    {
      "ref": "master",
      "name": "dev"
    },
    {
      "ref": "$release",
      "name": "stable"
    }
  ]
}
EOF
