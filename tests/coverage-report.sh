#!/bin/env bash

readonly test_config="$(pwd)/tests/files/xdg_config_home"

coverage_py () {
	if command -v coverage >/dev/null ; then
		coverage "$@"
		return $?
	fi
	python3-coverage "$@"
}

cd "$(git rev-parse --show-toplevel)" || exit
coverage_py erase
export SDOS_QUIET=1
XDG_CONFIG_HOME="$test_config" coverage_py run -m unittest discover -v -s tests
coverage_py report --fail-under=85 "$@"
