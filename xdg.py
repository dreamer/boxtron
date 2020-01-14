# Copyright (C) 2019-2020  Patryk Obara <patryk.obara@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

"""
XDG Base Directories

https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
"""

import os

DATA_HOME = os.environ.get('XDG_DATA_HOME') or \
            os.path.expanduser('~/.local/share')

CONF_HOME = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.expanduser('~/.config')

CACHE_HOME = os.environ.get('XDG_CACHE_HOME') or \
             os.path.expanduser('~/.cache')

DATA_DIRS = os.environ.get('XDG_DATA_DIRS', '/usr/share').split(os.pathsep)


def get_data_dirs(include_data_home=True):
    """Return all XDG_DATA_DIRS, optionally including XDG_DATA_HOME."""
    if include_data_home and DATA_HOME not in DATA_DIRS:
        return [DATA_HOME] + DATA_DIRS
    return DATA_DIRS


def cached_file(name):
    """Obtain path to cached file in application specific dir."""
    os.makedirs(CACHE_HOME + '/boxtron', exist_ok=True)
    return os.path.join(CACHE_HOME, 'boxtron', name)
