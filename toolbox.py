#!/usr/bin/env python3

"""
Useful functions and classes
"""

import os
import pathlib
import subprocess
import sys


def print_err(*value, sep=' ', end='\n', flush=False):
    """Prints the values to stderr."""
    print(*value, sep=sep, end=end, file=sys.stderr, flush=flush)


def enabled_in_env(var):
    """Returns True for environment variables with non-zero value."""
    val = os.environ.get(var)
    return val and val != '0'


def which(cmd):
    """Call which(1)."""
    try:
        out = subprocess.check_output(['which', cmd],
                                      stderr=subprocess.DEVNULL)
        return out.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None


def is_trivial_batch(file):
    """Test if file is trivially interpretable batch file."""
    if not file.lower().endswith('.bat'):
        return False
    if os.stat(file).st_size > 512:
        return False
    with open(file, 'r') as bat_file:
        lines = bat_file.readlines(512)
        return len(lines) <= 2
    return False


def read_trivial_batch(file):
    """Find DOSBox command in batch file and return its argument list."""
    with open(file, 'r') as bat_file:
        lines = bat_file.readlines(512)
        first_line = lines[0].strip().split(' ')
        if len(first_line) < 2:  # we expect at least "dosbox file.exe"
            return []
        win_path = pathlib.PureWindowsPath(first_line[0])
        cmd = win_path.parts[-1]
        if cmd.lower() in ('dosbox', 'dosbox.exe'):
            return first_line[1:]
    return []
