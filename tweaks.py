# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2019-2021  Patryk Obara <patryk.obara@gmail.com>

"""
Game-specific tweaks and workarounds
"""

import os
import pathlib
import re
import zipfile

import confgen
import toolbox
import xdg

from log import log_err
from winpathlib import to_posix_path

# There are several tweaks, that can be specified in TWEAKS_DB:
#
# download - describe files to download on the first start
# install  - name the function in tweaks module to finalize game installation
# midi     - see documentation for get_midi_preset
# conf     - dictionary of values to inject to DOSBox configuration
# commands - replace command line parameters used by specific game

TWEAKS_DB = {
    # The Ultimate DOOM
    'steam:2280': {
        'midi': 'auto',
    },
    # Final DOOM
    'steam:2290': {
        'midi': 'auto',
    },
    # DOOM II: Hell on Earth
    'steam:2300': {
        'midi': 'auto',
    },
    # Quake
    'steam:2310': {
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
    'steam:2360': {
        'midi': 'auto',
    },
    # HeXen: Deathkings of the Dark Citadel
    'steam:2370': {
        'midi': 'auto',
        'download': {
            'dkpatch.zip': {
                'txt': 'Original Patch 1.1',
                'url': 'http://www.gamers.org/pub/games/idgames/idstuff/hexen/dkpatch.zip',  # noqa pylint: disable=line-too-long
            },
        },
        'install': 'install_hexen_dk',
        'commands': {
            r'.*':  {
                'args': ['-c', 'mount C "base"',
                         '-c', 'C:',
                         '-c', 'PATCH.EXE',
                         '-c', 'HEXENDK.EXE',
                         '-c', 'exit'],
            },
        },
    },
    # Heretic: Shadow of the Serpent Riders
    'steam:2390': {
        'midi': 'auto',
    },
    # X-COM: Terror from the Deep
    'steam:7650': {
        'midi': 'auto',
        'conf': {
            'render': {'force_aspect': 'false'},
        },
    },
    # X-COM: UFO Defence / UFO: Enemy Unknown
    'steam:7760': {
        'midi': 'auto',
        'conf': {
            'render': {'force_aspect': 'false'},
        },
    },
    # Master Levels for DOOM II
    'steam:9160': {
        'midi': 'auto',
    },
    # STAR WARS™ - Dark Forces
    'steam:32400': {
        'midi': 'auto',
    },
    # Fallout: A Post Nuclear Role Playing Game
    'steam:38400': {
        'download': {
            'dos32a-912.zip': {
                'txt': 'DOS/32 Advanced DOS Extender',
                'url': 'http://download.narechk.net/dos32a-912-bin.zip',
            },
            'SETUP40.ZIP': {
                'txt': 'HMI Sound Setup',
                'url': 'http://www.r-t-c-m.com/knowledge-base/downloads-rtcm/tekwar-tools/SETUP40.ZIP',  # noqa pylint: disable=line-too-long
            },
            'fallout_patch_1_1_dos.zip': {
                'txt': 'Fallout patch 1.1 for DOS',
                'url': 'http://www.nma-fallout.com/resources/fallout-official-v1-1-patch-dos.49/download?version=50',  # noqa pylint: disable=line-too-long
            },
        },
        'install': 'install_fallout',
        'commands': {
            r'.*':  {
                'args': ['FALLOUT.EXE', '-exit'],
            },
        },
    },
    # Earthworm Jim
    'steam:38480': {
        'commands': {
            r'.*':  {
                'args': ['-conf', 'ewj1.conf'],
            },
        },
    },
    # Earthworm Jim 2
    'steam:38490': {
        'commands': {
            r'.*':  {
                'args': ['-conf', 'ewj2.conf'],
            },
        },
    },
    # Retro City Rampage™ DX
    'steam:204630': {
        'install': 'install_retro_city_rampage',
        'conf': {
            'render': {'force_aspect': 'false'},
        },
        'commands': {
            r'.*':  {
                'args': ['RCR486/RCR.EXE', '-exit'],
            },
        },
    },
    # STAR WARS™ - X-Wing Special Edition
    'steam:354430': {
        'midi': 'auto',
    },
    # Shadow Warrior (Classic)
    'steam:358400': {
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
    'steam:371180': {
        'midi': 'disable',
        'commands': {
            r'.*':  {
                'args': ['noah3dos.exe', '-exit'],
            },
        },
    },
    # System Shock: Classic
    'steam:410700': {
        'midi': 'auto',
    },
    # Tomb Raider I
    # As of 0.74-2, upstream DOSBox does not support GLide acceleration.
    # This tweak starts the game without hardware acceleration.
    'steam:224960': {
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
    'steam:225140': {
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
    'steam:283270': {
        'midi': 'auto',
    },
    # King's Table - The Legend of Ragnarok
    'steam:719310': {
        'midi': 'auto',
    },
    # MegaRace
    #
    # This game uses different .conf files depending on game language.
    # TODO provide fallback mechanism for missing .conf files or glob support
    #
    'steam:730580': {
        'midi': 'disable',
        'conf': {
            'sblaster': {'force_irq': '5'},
        },
        'commands': {
            r'.*':  {
                'args': ['Megarace.bat'],
            },
        },
    },
    # MegaRace 2
    'steam:733760': {
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
    # Leisure Suit Larry 1
    'steam:763970': {
        'commands': {
            r'.*':  {
                'args': ['-c', 'mount C .',
                         '-c', 'C:',
                         '-c', 'call SIERRA',
                         '-c', 'exit'],
            },
        },
    },
    # Leisure Suit Larry 2
    'steam:765840': {
        'commands': {
            r'.*':  {
                'args': ['SCIV.EXE', '-exit'],
            },
        },
    },
    # Leisure Suit Larry 3
    'steam:765850': {
        'commands': {
            r'.*':  {
                'args': ['SCIV.EXE', '-exit'],
            },
        },
    },
    # Leisure Suit Larry 5
    'steam:765860': {
        'commands': {
            r'.*':  {
                'args': ['SCIDHUV.EXE', '-exit'],
            },
        },
    },
    # Lords of the Realm
    'steam:254920': {
        'commands': {
            r'.*':  {
                'args': ['-c', 'mount C "../../Lords of the Realm I"',
                         '-c', 'C:',
                         '-c', 'lords.exe',
                         '-c', 'exit'],
            },
        },
    },
}  # yapf: disable


def command_tweak_needed(app_id):
    """Return true if game's command line needs to be changed."""
    return app_id in TWEAKS_DB and 'commands' in TWEAKS_DB[app_id]


def download_tweak_needed(app_id):
    """Return true if game needs to be download something for installation."""
    return app_id in TWEAKS_DB and 'download' in TWEAKS_DB[app_id]


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
    log_err('no suitable tweak found for:', cmd_line)
    return cmd_line[1:]


def install(app_id):
    """Call specific install function."""
    function_name = TWEAKS_DB[app_id]['install']
    installf = globals()[function_name]
    return installf()


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
    if toolbox.enabled_in_env('BOXTRON_NO_MIDI_PRESET', 'SDOS_NO_MIDI_PRESET'):
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
# broken path), then Boxtron and DOSBox are going to fail because .conf files
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

    dbox_args = confgen.parse_dosbox_arguments(args)  # throws RuntimeException
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
    return False, None


def install_test_42():
    """Dummy install function for testing purposes."""
    return 42


def install_retro_city_rampage():
    """Install Retro City Rampage™ DX DOS version.

    It is bundled with the Steam version, just needs to be unpacked.
    """
    if not os.path.isfile('other/RCR486_MS-DOS.zip'):
        toolbox.unzip('RetroCityRampage486_MS-DOS_v1.0.zip', 'other')
    if not os.path.isfile('RCR486/RCR.EXE'):
        toolbox.unzip('other/RCR486_MS-DOS.zip', 'RCR486')


def install_shadow_warrior():
    """Rename broken file causing crash for Shadow Warrior Classic (358400).
    """
    path = 'Shadow Warrior/SWP.cfg'
    if os.path.isfile(path):
        os.rename(path, path + '.bak')


def install_fallout():
    """Unpack patch file to get Fallout DOS binary.

    Assumes, that patch was already downloaded and placed in the cache.
    """

    if not os.path.isfile('DOS4GW.EXE_'):
        archive = zipfile.ZipFile(xdg.cached_file('dos32a-912.zip'), 'r')
        archive.extract('binw/dos32a.exe')
        archive.close()
        os.rename('binw/dos32a.exe', 'DOS4GW.EXE')
        os.rmdir('binw')

    if not os.path.isfile('HMIDET.386') or not os.path.isfile('HMIDRV.386'):
        archive = zipfile.ZipFile(xdg.cached_file('SETUP40.ZIP'), 'r')
        archive.extract('HMIDET.386')
        archive.extract('HMIDRV.386')
        archive.close()

    if not os.path.isfile('FALLOUT.EXE'):
        cache_file = xdg.cached_file('fallout_patch_1_1_dos.zip')
        toolbox.unzip(cache_file, 'patch_1_1_dos')
        toolbox.unzip('patch_1_1_dos/FALL11.ZIP', '.')

    rpatch = [
        'file:fallout.cfg',
        r's:/(art_cache_size=)(\d+)/\g<1>5/',
    ]
    toolbox.apply_resource_patch(rpatch)


def install_hexen_dk():
    """Fix music in HeXen: Deathkings of the Dark Citadel"""
    digest = 'ea5e34c9f7eb677c593f125a0c45db2aaf2d98b8f6e9d50bd683a655aeec531f'
    if toolbox.sha256sum('base/HEXDD.WAD') != digest:
        toolbox.unzip(xdg.cached_file('dkpatch.zip'), 'base')
