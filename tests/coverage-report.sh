#!/bin/env bash

cd "$(git rev-parse --show-toplevel)" || exit
coverage3 erase
for tfile in tests/test_*.py ; do
	PYTHONPATH=. coverage3 run "$tfile"
done
coverage3 report --fail-under=70 "$@"
