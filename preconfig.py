# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2019-2021  Patryk Obara <patryk.obara@gmail.com>

"""
Handle unpacking files for game pre-configuration.
"""

import os
import sys
import tarfile

import toolbox

CHECKSUM = 'c0452d6addcde172b71cac7b339e074f5f13a7ad83f2ee4736d47025dcbc760e'


def find_resource_file(prog=sys.argv[0]):
    """Return path to bundled resource file."""
    path, _ = os.path.split(os.path.abspath(prog))
    preconfig_file = os.path.join(path, 'preconfig.tar')
    try:
        if tarfile.is_tarfile(preconfig_file):
            return preconfig_file
    except FileNotFoundError:
        return None
    return None


def __checksum__():
    return toolbox.sha256sum(find_resource_file())


def verify():
    """Basic verification if file originates from release."""
    rfile = find_resource_file()
    assert rfile
    return toolbox.sha256sum(rfile) == CHECKSUM


def open_resource(file_name):
    """Open a ResourceFile."""
    return ResourceFile(file_name)


class ResourceFile:
    """Read and extract files from a resource file."""

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

    def includes(self, app_id) -> bool:
        """Return iff file contains setup for app_id."""
        pfx = 'preconfig/{}/'.format(app_id)
        return list(self.filter_pfx(pfx))

    def extract(self, app_id, resource):
        """Extract all files for named app_id and resource to working dir."""
        pfx = 'preconfig/{}/{}/'.format(app_id, resource)
        xlist = list(self.filter_pfx(pfx))
        for xfile in xlist:
            xfile.name = xfile.name.replace(pfx, '')
        self.tar.extractall(path='.', members=xlist, numeric_owner=True)

    def apply_rpatch(self, app_id, resource):
        """Apply resource patch if it exists."""
        path = 'preconfig/{}/{}.rpatch'.format(app_id, resource)
        files = list(self.filter_pfx(path))
        if not files:
            return
        assert files[0].isfile()
        rpatch = self.tar.extractfile(files[0])
        lines = rpatch.read().decode('utf-8').split('\n')
        toolbox.apply_resource_patch(lines)
