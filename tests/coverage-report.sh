#!/bin/env bash

coverage_py () {
	if command -v coverage >/dev/null ; then
		coverage "$@"
		return $?
	fi
	python3-coverage "$@"
}

cd "$(git rev-parse --show-toplevel)" || exit
coverage_py erase
coverage_py run -m unittest discover -v -s tests
coverage_py report --fail-under=80 "$@"
