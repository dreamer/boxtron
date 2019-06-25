#!/usr/bin/env python3

"""
Useful functions and classes
"""

import os
import pathlib
import re
import shlex
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
    if not os.path.isfile(file):
        return False
    if os.stat(file).st_size > 512:
        return False
    with open(file, 'r') as bat_file:
        lines = bat_file.readlines(512)
        return len(lines) <= 2
    return False


def argsplit_windows(line):
    """Convert Windows-style string to list of arguments."""

    def unquote(x):
        if len(x) >= 2 and x.startswith('"') and x.endswith('"'):
            return x[1:-1]
        return x

    return [unquote(x) for x in shlex.split(line, posix=False)]


def read_trivial_batch(file):
    """Find DOSBox command in batch file and return its argument list."""
    with open(file, 'r') as bat_file:
        lines = bat_file.readlines(512)
        first_line = argsplit_windows(lines[0])
        assert first_line, 'error processing .bat file (not enough words)'
        win_path = pathlib.PureWindowsPath(first_line[0])
        cmd = win_path.parts[-1]
        if cmd.lower() in ('dosbox', 'dosbox.exe'):
            return first_line[1:]
    assert False, 'error processing .bat file'
    return []


def sed(filename, regex_find, regex_replace):
    """Edit file in place."""
    with open(filename, 'r+') as txt:
        data = txt.read()
        txt.seek(0)
        txt.write(re.sub(regex_find, regex_replace, data))
        txt.truncate()


def apply_resource_patch(lines):
    """Edit files with instructions from resource patch file."""
    file = None
    for line in lines:
        cmd = line.strip()
        if not cmd:
            continue
        if cmd.startswith('file:'):
            file = cmd[5:]
            continue
        if cmd.startswith('s:'):
            assert file
            separator = cmd[2]
            regex_1_end = cmd.find(separator, 3)
            regex_2_end = cmd.find(separator, regex_1_end + 1)
            assert regex_1_end > 2
            assert regex_2_end > regex_1_end
            regex_1 = cmd[3:regex_1_end]
            regex_2 = cmd[regex_1_end + 1:regex_2_end]
            sed(file, regex_1, regex_2)
            continue
        raise ValueError('Unexpected instruction: {}'.format(cmd))


class PidFile:
    """Helper class to create and remove PID file"""

    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        with open(self.file_name, 'w') as pid_file:
            pid_file.write(str(os.getpid()))
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        try:
            os.remove(self.file_name)
        except FileNotFoundError:
            pass
