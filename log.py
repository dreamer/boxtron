#!/usr/bin/python3

"""
Log functions
"""
import sys

import toolbox

PREFIX = 'boxtron:'

QUIET = toolbox.enabled_in_env('SDOS_QUIET')


def print_err(*value, sep=' ', end='\n', flush=False):
    """Prints the values to stderr."""
    if QUIET:
        return
    print(*value, sep=sep, end=end, file=sys.stderr, flush=flush)


def log(*value, sep=' ', end='\n', flush=False):
    """Prints the values to stderr with prefix."""
    print_err(PREFIX, *value, sep=sep, end=end, flush=flush)


def log_err(*value, sep=' ', end='\n', flush=False):
    """Prints the values to stderr with prefix and 'error:'"""
    log('error:', *value, sep=sep, end=end, flush=flush)


def log_warn(*value, sep=' ', end='\n', flush=False):
    """Prints the values to stderr with prefix and 'warning:'"""
    log('warning:', *value, sep=sep, end=end, flush=flush)
