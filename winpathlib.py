#!/usr/bin/env python3

"""
Module providing conversion between DOS/Windows and Posix paths.
"""

import os
import pathlib


def to_posix_path(windows_path_str):
    """Convert a string representing case-insensitive path to a string
    representing path to an existing file.
    """
    if windows_path_str == '.':
        return '.'

    win_path = pathlib.PureWindowsPath(windows_path_str)

    xs = list(__posix_paths_matching__(win_path.parts))
    if xs:
        return xs[0]
    return None


def __posix_paths_matching__(parts):
    if parts == ():
        yield ''
        return
    prefix_parts, last_part = parts[:-1], parts[-1]
    for prefix in __posix_paths_matching__(prefix_parts):
        if last_part in ('.', '..'):
            yield os.path.join(prefix, last_part)
            continue
        for candidate in os.listdir(prefix or '.'):
            if candidate.casefold() == last_part.casefold():
                yield os.path.join(prefix, candidate)
