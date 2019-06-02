#!/usr/bin/env python3

"""
Module providing conversion between DOS/Windows and Posix paths.
"""

import os
import pathlib


def to_posix_path(windows_path_str):
    """Convert a string representing case-insensitive path to a string
    representing path to existing file.
    """
    if windows_path_str == '.':
        return '.'
    win_path = pathlib.PureWindowsPath(windows_path_str)
    posix_parts = to_posix_parts(win_path.parts)
    if posix_parts is None:
        return None
    if posix_parts == ():
        return ''
    return os.path.join(*posix_parts)


def guess(part):
    """Generate all the possible capitalizations of given string,
    starting with the most probable ones.
    """
    yield part
    yield part.upper()
    yield part.lower()
    yield part.capitalize()

    def switch_cases(txt):
        if not txt:
            return ['']
        letter = txt[0]
        rest = switch_cases(txt[1:])
        return [letter.upper() + suffix for suffix in rest] + \
               [letter.lower() + suffix for suffix in rest]

    for candidate in switch_cases(part):
        yield candidate


def to_posix_parts(parts):
    """Return posix path representing existing file referenced in
    case-insensitive path passed as tuple.

    Works with assumption, that existing file is unique.
    """
    # TODO rewrite this in more time-effective manner for worst case scenario.
    if parts is None:
        return None
    if parts == ():
        return parts
    prefix_parts, last_part = parts[:-1], parts[-1]
    prefix = to_posix_parts(prefix_parts)
    if prefix is None:
        return None
    for case_sensitive_part in guess(last_part):
        case_sensitive_parts = prefix + (case_sensitive_part,)
        if os.path.exists(os.path.join(*case_sensitive_parts)):
            return case_sensitive_parts
    return None
