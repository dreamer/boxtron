#!/bin/bash

# Copyright (C) 2019 Patryk Obara <patryk.obara@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

codestyle_py () {
	if command -v pycodestyle >/dev/null ; then
		pycodestyle "$@"
		return $?
	fi
	pycodestyle-3 "$@"
}

codestyle_py "$@"
