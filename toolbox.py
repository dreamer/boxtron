#!/usr/bin/env python3

"""
Useful functions and classes
"""

import os
import subprocess
import sys


def print_err(*value, sep=' ', end='\n', flush=False):
    """Prints the values to sys.stderr"""
    print(*value, sep=sep, end=end, file=sys.stderr, flush=flush)


def enabled_in_env(var):
    """Returns True for env variables with nonzero value."""
    val = os.environ.get(var)
    return val and val != '0'


def which(cmd):
    """Call which(1)."""
    try:
        return subprocess.check_output(['which', cmd]).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None
