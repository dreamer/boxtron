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
