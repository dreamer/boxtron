#!/usr/bin/env python3

"""
Useful functions and classes
"""

import sys


def print_err(*value, sep=' ', end='\n', flush=False):
    """Prints the values to sys.stderr"""
    print(*value, sep=sep, end=end, file=sys.stderr, flush=flush)
