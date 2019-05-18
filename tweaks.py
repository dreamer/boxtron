#!/usr/bin/env python3

"""
Game-specific tweaks and workarounds

"""

import re
from toolbox import print_err

TWEAKS_DB = {
    # Jagged Alliance Gold
    '283270': {
        'commands': {
            r'.*/Jagged Alliance/run.bat': {
                'args': ['-c', 'mount C Installed',
                         '-c', 'imgmount D cd.iso -t cdrom',
                         '-c', 'C:',
                         '-c', 'cd jagged',
                         '-c', 'ja.bat'],
            },
            r'.*/Jagged Alliance Deadly Games/run.bat': {
                'args': ['-c', 'mount C Installed',
                         '-c', 'imgmount D cd.iso -t cdrom',
                         '-c', 'C:',
                         '-c', 'cd deadly',
                         '-c', 'deadly.bat'],
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
    print_err('run_dosbox: error: no suitable tweak found for:', cmd_line)
    return []
