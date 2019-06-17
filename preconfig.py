#!/usr/bin/env python3

"""
Handle unpacking files for game pre-configuration.

"""

import os
import sys
import tarfile
import hashlib


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


def verify():
    """Basic verification if file originates from release."""
    rfile = find_resource_file()
    assert rfile
    sha1sum = hashlib.sha1()
    with open(find_resource_file(), 'rb') as tar:
        block = tar.read()
        sha1sum.update(block)
    return sha1sum.hexdigest() == '65fa262a429213eea6f50774e6885d5393d2599f'


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

    def includes(self, app_id):
        """Return iff file contains setup for app_id."""
        pfx = 'preconfig/{}/'.format(app_id)
        return list(self.filter_pfx(pfx)) != []

    def extract(self, app_id, resource):
        """Extract all files for named app_id and resource to working dir."""
        pfx = 'preconfig/{}/{}/'.format(app_id, resource)
        xlist = list(self.filter_pfx(pfx))
        for xfile in xlist:
            xfile.name = xfile.name.replace(pfx, '')
        self.tar.extractall(path='.', members=xlist, numeric_owner=True)
