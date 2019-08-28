#!/usr/bin/python3

"""
TODO module description
"""

import os

# Things to consider before I forget them again:
#
# - referenced path is not guaranteed to be a cue file at all
#   often it will be an ISO image or maybe other binary blob
#
# - for cue file we don't really need proper parser -
#   we only need a filter that can transform file names inside a cue file
#


def is_cue_file(path):
    """Simple heuristic to determine if a path points to .cue file"""
    if not os.path.isfile(path):
        return False
    if os.stat(path).st_size > 4096:
        return False
    with open(path, 'r') as cue_file:
        lines = cue_file.readlines(4096)
        if len(lines) < 3:
            return False
        first_line = lines[0].strip()
        return first_line.startswith('FILE ')
    return False


def parse_cue_file(path):
    """TODO"""
    assert path
