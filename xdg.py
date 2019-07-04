#!/usr/bin/python3

"""
XDG Base Directories

https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
"""
import os

CONF_HOME = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.expanduser('~/.config')

DATA_HOME = os.environ.get('XDG_DATA_HOME') or \
            os.path.expanduser('~/.local/share')
