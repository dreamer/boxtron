#!/usr/bin/python3

"""
Game-specific tweaks and workarounds

"""

import os
import pathlib
import re
import zipfile

import confgen

from toolbox import print_err, enabled_in_env
from winpathlib import to_posix_path

TWEAKS_DB = {
    # The Ultimate DOOM
    '2280': {
        'midi': 'auto',
        'conf': {
            'render': {'aspect': 'true'},
        },
    },
    # Final DOOM
    '2290': {
        'midi': 'auto',
    },
    # DOOM II: Hell on Earth
    '2300': {
        'midi': 'auto',
    },
    # Quake
    '2310': {
        'commands': {
            r'.*':  {
                'args': ['-c', 'mount C .',
                         '-c', 'C:',
                         '-c', 'quake.exe -nocdaudio',
                         '-c', 'exit'],
            },
        },
    },
    # HeXen: Beyond Heretic
    '2360': {
        'midi': 'auto',
    },
    # Heretic: Shadow of the Serpent Riders
    '2390': {
        'midi': 'auto',
    },
    # X-COM: Terror from the Deep
    '7650': {
        'midi': 'auto',
    },
    # X-COM: UFO Defence / UFO: Enemy Unknown
    '7760': {
        'midi': 'auto',
    },
    # Master Levels for DOOM II
    '9160': {
        'midi': 'auto',
    },
    # King's Quest™ Collection
    '10100': {
        'conf': {
            'render': {'aspect': 'true'},
        },
    },
    # STAR WARS™ - Dark Forces
    '32400': {
        'midi': 'auto',
        'conf': {
            'render': {'aspect': 'true'},
        },
    },
    # Retro City Rampage™ DX
    '204630': {
        'install': 'install_retro_city_rampage',
        'commands': {
            r'.*':  {
                'args': ['RCR486/RCR.EXE', '-exit'],
            },
        },
    },
    # STAR WARS™ - X-Wing Special Edition
    '354430': {
        'midi': 'auto',
    },
    # Shadow Warrior (Classic)
    '358400': {
        'install': 'install_shadow_warrior',
        'midi': 'disable',
        'commands': {
            r'.*Shadow Warrior - Dos.bat':  {
                'args': ['-conf', 'Shadow Warrior\\SW.conf', '-noautoexec',
                         '-c', 'mount C "Shadow Warrior"',
                         '-c', 'imgmount D "Shadow Warrior\\shadow.cue" -t iso',
                         '-c', 'C:',
                         '-c', 'SwDOS.exe',
                         '-c', 'exit'],
            },
        },
    },
    # Super 3D Noah's Ark
    '371180': {
        'midi': 'disable',
        'commands': {
            r'.*':  {
                'args': ['noah3dos.exe', '-exit'],
            },
        },
    },
    # System Shock: Classic
    '410700': {
        'midi': 'auto',
    },
    # Tomb Raider I
    # As of 0.74-2, upstream DOSBox does not support GLide acceleration.
    # This tweak starts the game without hardware acceleration.
    '224960': {
        'commands': {
            r'.*':  {
                'args': ['-conf', 'dosboxtr.conf', '-noautoexec',
                         '-c', 'mount C .',
                         '-c', 'imgmount D GAME.DAT -t iso -fs iso',
                         '-c', 'C:',
                         '-c', 'cd TOMBRAID',
                         '-c', 'TOMBNO~1.EXE',
                         '-c', 'exit'],
            },
        },
    },
    # Duke Nukem 3D (Classic)
    '225140': {
        'midi': 'auto',
        'commands': {
            r'.*bin/dosbox/dosbox\.exe':  {
                'args': ['-conf', 'dosbox.conf', '-noautoexec',
                         '-c', 'mount C .',
                         '-c', 'C:',
                         '-c', 'DUKE3D.EXE',
                         '-c', 'exit'],
            },
        },
    },
    # Jagged Alliance Gold
    # Jagged Alliance Deadly Games
    '283270': {
        'midi': 'auto',
    },
    # MegaRace 2
    '733760': {
        'midi': 'disable',
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
}  # yapf: disable


def command_tweak_needed(app_id):
    """Return true if game's command line needs to be changed."""
    return app_id in TWEAKS_DB and 'commands' in TWEAKS_DB[app_id]


def install_tweak_needed(app_id):
    """Return true if game needs to be installed before start."""
    return app_id in TWEAKS_DB and 'install' in TWEAKS_DB[app_id]


def tweak_command(app_id, cmd_line):
    """Convert command line based on TWEAKS_DB."""
    assert len(cmd_line) >= 1
    orig_cmd = ' '.join(cmd_line)
    exec_replacements = TWEAKS_DB[app_id]['commands']
    for expr, replacement in exec_replacements.items():
        exe_pattern = re.compile(expr)
        if exe_pattern.match(orig_cmd):
            if 'args' in replacement:
                return replacement['args']
            raise KeyError
    print_err('steam-dos: error: no suitable tweak found for:', cmd_line)
    return cmd_line[1:]


def install(app_id):
    """Call specific install function."""
    function_name = TWEAKS_DB[app_id]['install']
    installf = globals()[function_name]
    installf()


def get_conf_tweak(app_id):
    """Return dictionary used to overwrite publisher-supplied defaults.

    Use this tweak for games, where defaults are clearly wrong.
    """
    if app_id not in TWEAKS_DB:
        return {}
    if 'conf' not in TWEAKS_DB[app_id]:
        return {}
    return TWEAKS_DB[app_id]['conf']


def get_midi_preset(app_id):
    """Return MIDI preset for given AppID.

    Possible return values:

    enable  - (default) turn on software midi synthesiser
    disable - game does not support midi at all
    auto    - pre-configure game to automatically turn midi on/off depending
              on user preference
    """
    if enabled_in_env('SDOS_NO_MIDI_PRESET'):
        return 'enable'
    if app_id not in TWEAKS_DB:
        return 'enable'
    if 'midi' not in TWEAKS_DB[app_id]:
        return 'enable'
    return TWEAKS_DB[app_id]['midi']


# Normally, Steam is changing working dir to the sub-directory of game
# installation dir (which is specified by the game publisher) and then runs
# command as an absolute path.
#
# If Steam fails to chdir into the correct directory before running the game
# (which might happen - either as a result of Steam bug or publisher submitting
# broken path), then steam-dos and DOSBox are going to fail because .conf files
# will not be in their expected location.
#
def check_cwd(command_line):
    """Test if current working directory is appropriate to launch the game.

    Returns (False, path) if all .conf files referenced in dosbox command line
    can be found (path is the same as current working dir in such case).

    Returns (True, path) if all .conf files can be found in path, and path
    is not a working dir (changing dir is required).

    Returns (False, None) if .conf files couldn't be found at all.
    """
    prog, args = command_line[0], command_line[1:]
    prog_path = pathlib.PurePosixPath(prog)
    if not prog_path.is_absolute():
        return False, None

    dbox_args = confgen.parse_dosbox_arguments(args)
    conf_paths = (dbox_args.conf or [])

    def paths_found():
        return all(to_posix_path(p, strict=False) for p in conf_paths)

    if paths_found():
        return False, os.getcwd()

    orig_cwd = os.getcwd()

    prefix = str(prog_path)
    while True:
        prefix, _ = os.path.split(prefix)
        os.chdir(prefix)
        if paths_found():
            os.chdir(orig_cwd)
            return True, prefix
        if prefix in (os.path.expanduser('~'), '/'):
            break

    os.chdir(orig_cwd)
    return False, None  # TODO show nice error to the user


def install_retro_city_rampage():
    """Install Retro City Rampage™ DX DOS version.

    It is bundled with the Steam version, just needs to be unpacked.
    """
    if not os.path.isfile('other/RCR486_MS-DOS.zip'):
        archive = zipfile.ZipFile('RetroCityRampage486_MS-DOS_v1.0.zip', 'r')
        archive.extractall('other')
        archive.close()
    if not os.path.isfile('RCR486/RCR.EXE'):
        archive = zipfile.ZipFile('other/RCR486_MS-DOS.zip', 'r')
        archive.extractall('RCR486')
        archive.close()


def install_shadow_warrior():
    """Rename broken file causing crash for Shadow Warrior Classic (358400).
    """
    path = 'Shadow Warrior/SWP.cfg'
    if os.path.isfile(path):
        os.rename(path, path + '.bak')

