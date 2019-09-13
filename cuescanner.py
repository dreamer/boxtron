#!/usr/bin/python3

"""
Simple introspection and filtering of .cue files.
"""

import os
import re

import winpathlib


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


def list_file_entries(cue_path):
    """Return iterator over file entries"""
    with open(cue_path, 'r') as cue_file:
        pattern_1 = r' *FILE +"([^"]+)" +(.*)'
        pattern_2 = r' *FILE +([^ ]+) +(.*)'
        file_entry_1 = re.compile(pattern_1)
        file_entry_2 = re.compile(pattern_2)
        for line in cue_file:
            match = file_entry_1.match(line) or file_entry_2.match(line)
            if match:
                file_path = match.group(1)
                file_type = match.group(2)
                yield file_path, file_type


def valid_cue_file_paths(cue_path):
    """Return true if all paths in a .cue file refer to existing files"""

    cue_dir, _ = os.path.split(cue_path)

    def is_file(file_entry):
        path, _ = file_entry
        ref_file = os.path.join(cue_dir, path)
        return os.path.isfile(ref_file)

    return all(map(is_file, list_file_entries(cue_path)))


def create_fixed_cue_file(cue_path, new_path):
    """Filter content of .cue file and save as fixed file"""
    with open(cue_path, 'r') as cue_file, open(new_path, 'w') as out_file:
        pattern_1 = r'( *)FILE +"([^"]+)" +(.*)'
        pattern_2 = r'( *)FILE +([^ ]+) +(.*)'
        file_entry_1 = re.compile(pattern_1)
        file_entry_2 = re.compile(pattern_2)
        for line in cue_file:
            match = file_entry_1.match(line) or file_entry_2.match(line)
            if match:
                space_pfx = match.group(1)
                file_path = winpathlib.to_posix_path(match.group(2))
                file_type = match.group(3)
                out_file.write('{}FILE "{}" {}\n'.format(
                    space_pfx, file_path, file_type))
            else:
                out_file.write(line)
