#!/usr/bin/env python3

"""
Handle unpacking files for game pre-configuration.

"""

import os
import sys
import tarfile


def find_resource_file():
    """TODO."""
    assert sys.argv
    path, _ = os.path.split(os.path.abspath(sys.argv[0]))
    preconfig_file = os.path.join(path, 'preconfig.tar')
    if not tarfile.is_tarfile(preconfig_file):
        return None
    preconfig = tarfile.open(preconfig_file, mode='r:')
    preconfig.list(True)
    pfx = 'preconfig/32400/midi_off/'
    xfilter = filter(lambda x: x.name.startswith(pfx), preconfig.members)
    xlist = list(xfilter)
    for xfile in xlist:
        xfile.name = xfile.name.replace(pfx, '')
    preconfig.extractall(path='game_dir', members=xlist, numeric_owner=True)
    return preconfig


def open_resource(file_name):
    """Open a ResourceFile."""
    return ResourceFile(file_name)


class ResourceFile:
    """TODO."""

    def __init__(self, file_name):
        self.file_name = file_name
        self.tar = None
        self.members = []

    def __enter__(self):
        self.tar = tarfile.open(self.file_name, mode='r:')
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.tar.close()

    def filter_pfx(self, pfx):
        """Return iterator over objects named with prefix."""
        return filter(lambda x: x.name.startswith(pfx), self.tar.getmembers())

    def includes(self, app_id):
        """Return iff file contains setup for app_id."""
        pfx = 'preconfig/{}/'.format(app_id)
        return list(self.filter_pfx(pfx)) != []
