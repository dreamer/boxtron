#!/bin/env bash

cd "$(git rev-parse --show-toplevel)" || exit
python3-coverage erase
python3-coverage run -m unittest discover -v -s tests
python3-coverage report --fail-under=80 "$@"
