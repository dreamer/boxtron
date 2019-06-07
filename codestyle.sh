#!/bin/env bash

codestyle_py () {
	if command -v pycodestyle >/dev/null ; then
		pycodestyle "$@"
		return $?
	fi
	pycodestyle-3 "$@"
}

codestyle_py "$@"
