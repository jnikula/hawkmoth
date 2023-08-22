#!/bin/bash
# Copyright (c) 2023, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

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
