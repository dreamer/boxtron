#!/usr/bin/python3

"""
Useful functions and classes
"""

import hashlib
import os
import pathlib
import re
import shlex
import subprocess
import sys
import zipfile

import winpathlib


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


def relative_path_to(pwd, file_path):
    """Return relative path to a file."""
    abs_path = os.path.abspath(file_path)
    common_prefix = os.path.commonpath([abs_path, pwd])
    relative_suffix = abs_path[len(common_prefix) + 1:]
    relative_suffix_pwd = pwd[len(common_prefix) + 1:]
    relative_suffix_pwd_dirs = relative_suffix_pwd.split(os.path.sep)
    dirs_up = ['../' for _ in filter(lambda x: x, relative_suffix_pwd_dirs)]
    relative_up = ''.join(dirs_up)
    dot_path = './{}{}'.format(relative_up, os.path.dirname(relative_suffix))
    return dot_path if dot_path.endswith('/') else dot_path + '/'


def expand_batch_variables(file_path, line):
    """Expand variables with modifier.

    Full support for all variables is not planned; check Microsoft
    documentation for full list ("Variable with modifier"):

    https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-xp/bb490909(v=technet.10)
    """
    # %~dp0 -> expands to drive letter followed by path to the batch file
    #          (sans file name); I don't support conversion with driver letter
    #          so will convert it to relative path for now:
    dp0_path = relative_path_to(os.getcwd(), file_path)
    return line.replace('%~dp0', dp0_path.replace('/', '\\'))


def read_trivial_batch(file):
    """Find DOSBox command in batch file and return its argument list.

    Returns a tuple:

    The first element is a directory used by batch file to invoke DOSBox.
    If batch contains no relevant information, it's 'None'.  The second element
    is an argument list.
    """
    line_num = 1
    with open(file, 'r') as bat_file:
        lines = bat_file.readlines(512)
        assert lines, 'error processing .bat file (not enough lines)'
        new_path = None
        for line in lines:
            expanded_line = expand_batch_variables(file, line)
            this_line = argsplit_windows(expanded_line)
            if not this_line:
                continue
            first_word = this_line[0]
            if first_word.lower() in ('echo', '@echo'):
                continue
            if first_word.lower() in ('cd', '@cd'):
                # This works only for a single 'CD', but no game uses more than
                # one (so far).  If we'll ever find one, then it's time to
                # implement more serious batch interpreter instead.
                new_path = winpathlib.to_posix_path(this_line[1])
                assert new_path, 'error processing .bat ' + \
                                 'file: no directory named ' + \
                                 '{}'.format(this_line[1])
            win_path = pathlib.PureWindowsPath(first_word)
            exe = win_path.parts[-1]
            if exe.lower() in ('dosbox', 'dosbox.exe'):
                return new_path, this_line[1:]
    assert False, 'error processing .bat file (line {})'.format(line_num)
    return None, []


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
        # skip over empty lines and comments
        if not cmd or cmd.startswith('#'):
            continue
        # assign a file, but only if it exists
        if cmd.startswith('file:'):
            path = cmd[5:]
            file = path if os.path.isfile(path) else None
            continue
        # modify a file, if it exists
        if cmd.startswith('s:'):
            if file is None:
                continue
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


def guess_game_install_dir(directory=None):
    """Return absolute path pointing to game installation directory.

    Path will be escaped in a way, that allows it to be injected into
    quoted shell commands.

    This function assumes current working directory is a subdirectory
    of an installation directory.
    """
    path = directory or os.getcwd()
    posix_path = pathlib.PurePosixPath(path)
    assert posix_path.is_absolute()
    posix_parts = posix_path.parts
    steam_lib_pattern = ('steamapps'.casefold(), 'common'.casefold())
    share_games_pattern = ('share', 'games')
    lib_pattern_found, pos = False, -1
    prev_part_2, prev_part_1, this_part = '', '', ''
    for i, part in enumerate(posix_parts):
        prev_part_2 = prev_part_1
        prev_part_1 = this_part
        this_part = part.casefold()
        if steam_lib_pattern == (prev_part_2, prev_part_1) or \
           share_games_pattern == (prev_part_2, prev_part_1):
            lib_pattern_found = True
            pos = i
            break
    if not lib_pattern_found:
        return None
    found_path = os.path.join(*posix_parts[:pos + 1])
    return found_path.replace(' ', r'\ ').replace('&', r'\&')


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


def unzip(src_file, dst_dir):
    """Simply unzip a file."""
    archive = zipfile.ZipFile(src_file, 'r')
    archive.extractall(dst_dir)
    archive.close()


def sha256sum(path):
    """Simply compute sha256sum of a file."""
    algo = hashlib.sha256()
    with open(path, 'rb') as file:
        block = file.read()
        algo.update(block)
    return algo.hexdigest()
