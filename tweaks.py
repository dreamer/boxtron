#!/usr/bin/env python3

"""
Game-specific tweaks and workarounds

"""

import re
from toolbox import print_err

TWEAKS_DB = {
    # DOOM II: Hell on Earth
    '2300': {
        'commands': {
            r'.*doom2 \+ mouse.bat$':  {
                'args': ['-conf', 'base\\doom2m.conf'],
            },
            r'.*doom2.bat$': {
                'args': ['-conf', 'base\\doom2.conf'],
            },
        },
    },
    # MegaRace 2
    '733760': {
        'commands': {
            r'.*':  {
                'args': ['-conf', 'dosboxmegarace2.conf', '-noautoexec',
                         '-c', 'mount C .',
                         '-c', 'mount D . -t cdrom',
                         '-c', 'C:',
                         '-c', 'MEGARACE.EXE',
                         '-c', 'exit'],
            },
        },
    },
}


def tweak_command(app_id, cmd_line):
    """Convert command line based on TWEAKS_DB."""
    orig_cmd = ' '.join(cmd_line)
    exec_replacements = TWEAKS_DB[app_id]['commands']
    for expr, replacement in exec_replacements.items():
        exe_pattern = re.compile(expr)
        if exe_pattern.match(orig_cmd):
            if 'args' in replacement:
                return replacement['args']
            raise KeyError
    print_err('run_dosbox: warning: no suitable command tweak found')
    return []
