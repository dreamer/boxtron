#!/usr/bin/python3

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


def cached_file(name):
    """Obtain path to cached file in application specific dir."""
    os.makedirs(CACHE_HOME + '/steam-dos', exist_ok=True)
    return os.path.join(CACHE_HOME, 'steam-dos', name)
