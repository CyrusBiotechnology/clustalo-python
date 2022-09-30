#!/usr/bin/env bash

if [[ $(git branch --show-current) == "master" ]]; then
    git tag "$(cat VERSION)"
    git push --tags
else
    echo "MUST BE ON 'master' branch"
    exit 1
fi
