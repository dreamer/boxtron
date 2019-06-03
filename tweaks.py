#!/usr/bin/env python3

"""
Game-specific tweaks and workarounds

"""

import re
from toolbox import print_err

TWEAKS_DB = {
    # Duke Nukem 2
    '240180': {
        'chdir': True,
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


def workdir_tweak_needed(app_id):
    """Return true if game's working directory needs to be changed."""
    return app_id in TWEAKS_DB and 'chdir' in TWEAKS_DB[app_id]


def command_tweak_needed(app_id):
    """Return true if game's command line needs to be changed."""
    return app_id in TWEAKS_DB and 'commands' in TWEAKS_DB[app_id]


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
