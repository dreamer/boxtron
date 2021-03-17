#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2019-2021  Patryk Obara <patryk.obara@gmail.com>

codestyle_py () {
	if command -v pycodestyle >/dev/null ; then
		pycodestyle "$@"
		return $?
	fi
	pycodestyle-3 "$@"
}

codestyle_py "$@"
