#!/bin/env bash

cd "$(git rev-parse --show-toplevel)" || exit
coverage3 erase
coverage3 run -m unittest discover -v -s tests
coverage3 report --fail-under=70 "$@"
