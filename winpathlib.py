# Copyright (C) 2019-2020  Patryk Obara <patryk.obara@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Module providing conversion between DOS/Windows and Posix paths.
"""

import os
import pathlib


def to_posix_path(windows_path_str, *, strict=True):
    """Convert a string representing case-insensitive path to a posix path
    to an existing file or directory.

    Return None when there's no file nor directory, that could be
    referenced as this windows path.

    If windows path is ambiguous and can be mapped to more than one
    file, then raise FileNotFoundError.  When strict is set to False, then
    first file will be returned instead.
    """
    if windows_path_str == '.':
        return '.'
    win_path = pathlib.PureWindowsPath(windows_path_str)
    paths = __posix_paths_matching__(win_path.parts)
    path_1 = next(paths, None)
    path_2 = next(paths, None)
    if strict and path_2 is not None:
        err = "Windows path '{}' is ambiguous. " \
              "It can be '{}' or '{}'.".format(win_path, path_1, path_2)
        raise FileNotFoundError(err)
    return path_1


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
