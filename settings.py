# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2019-2021  Patryk Obara <patryk.obara@gmail.com>

"""
Settings file creation and handling.
"""

# pylint: disable=missing-docstring

import configparser
import os
import shlex
import itertools

import xdg
import xlib

from log import log, log_err, log_warn
from toolbox import enabled_in_env

SETTINGS_FILE = os.path.join(xdg.CONF_HOME, 'boxtron.conf')

DEFAULT_CONFGEN_FORCE = False

DEFAULT_MIDI_ENABLE = True

DEFAULT_MIDI_TOOL = 'timidity'

DEFAULT_MIDI_SEQ_REGEX = r''

DEFAULT_SOUNDFONT = 'FluidR3_GM.sf2'

BACKUP_SOUNDFONTS = ['FluidR3.sf2', 'FluidR3_GM2-2.sf2']

DEFAULT_DOSBOX_BINARY = 'dosbox'

DEFAULT_FULLSCREEN_MODE = 'screen 0'

DEFAULT_SCALER = 'normal3x'

DEFAULT_SETTINGS = """
[confgen]
# Set this value to 'true' if you want Boxtron to re-create DOSBox
# configuration on every run.
force = {confgen_force}

[midi]
# You can disable MIDI support here.
enable = {midi_enable}

# Select preferred software synthesiser here.
# Can be either 'timidity' or 'fluidsynth'
synthesiser = {midi_tool}

# You can name your preferred MIDI synthesiser here to override the one
# picked by default. If not found then software synthesiser will be
# started as a fallback.
#
# Value is treated as a regular expression using Python syntax, matched
# against the name of a MIDI client (case-insensitive); to list MIDI clients
# connected, use: $ aconnect -l
#
# For example, to match client named 'CASIO USB-MIDI', you can use
# value 'casio'.
#
# You can override this per-game with BOXTRON_USE_MIDI_SEQ environment variable.
#
# use_sequencer =

# Boxtron will look for a soundfont in following directories:
# /usr/share/soundfonts/
# /usr/share/sounds/sf2/
# /usr/local/share/soundfonts/
# /usr/local/share/sounds/sf2/
# ~/.local/share/sounds/sf2/  (or wherever XDG_DATA_HOME points)
# ~/.local/share/soundfonts/  (or wherever XDG_DATA_HOME points)
soundfont = {midi_soundfont}

[dosbox]
# Available modes:
# - screen 0, screen 1, etc:
#   The game will use fullscreen on selected screen, without changing
#   the native resolution of your display.  Mouse will be locked to the screen.
#   Default is 'screen 0', which is your primary display.
#   You can override this selection per-game with BOXTRON_SCREEN environment
#   variable, e.g: 'BOXTRON_SCREEN=2 %command%'
# - desktop:
#   The whole desktop area will be used (all displays) with the game centred,
#   the native resolution of your displays will be preserved.
# - disabled:
#   Start DOSBox in windowed modeby default.
fullscreenmode = {fullscreen_mode}

# Pick the default scaler, that you want to use for all games.
# You can override selection per-game by changing option render.scaler in file
# boxtron_<appid>_<id>.conf in game's installation dir.
# Here's comparison of different scalers: https://www.dosbox.com/wiki/Scaler
scaler = {scaler}

# Uncomment following line to specify a different DOSBox build:
{cmd_example}
"""


class Settings():

    def __init__(self, conf=None):
        self.store = configparser.ConfigParser(interpolation=None)
        self.store.add_section('confgen')
        self.store.add_section('midi')
        self.store.add_section('dosbox')
        self.store.read(conf or SETTINGS_FILE)
        self.fullresolution = 'desktop'
        self.finalized = False
        self.distdir = os.path.dirname(os.path.abspath(__file__))

    def setup(self):
        """Finalise settings initialisation on request.

        Some settings need more involved initialisation/detection procedure,
        which might fail or leave extensive logs on stderr.  We want this
        part of settings initialisation only when actually needed.
        """
        self.__setup_fullscreen__()
        midi_on = self.get_midi_on()
        if midi_on:
            self.__assure_sf2_exists__()
        self.finalized = True

    def __setup_fullscreen__(self):
        user_choice = self.get_dosbox_fullscreenmode()
        env_override = 'BOXTRON_SCREEN' in os.environ or \
                       'SDOS_SCREEN' in os.environ or \
                       'SDL_VIDEO_FULLSCREEN_DISPLAY' in os.environ or \
                       'SDL_VIDEO_FULLSCREEN_HEAD' in os.environ

        if user_choice in ('desktop', 'disabled') and not env_override:
            return

        screen = self.__get_screen_number__()
        all_screens = xlib.query_screens()

        if all_screens == {}:
            log_err('no screens detected')
        for number, info in all_screens.items():
            log("screen '{}': {}x{}".format(number, info.width, info.height))

        if screen not in all_screens:
            log("screen '{}' not found".format(screen))
            if '0' in all_screens:
                screen = '0'
                log("using '" + screen + "' instead")
            else:
                log("using desktop as screen instead")
                return

        log("selected screen '{}'".format(screen))
        os.putenv('SDL_VIDEO_FULLSCREEN_DISPLAY', screen)  # SDL >= 1.2.14
        os.putenv('SDL_VIDEO_FULLSCREEN_HEAD', screen)  # SDL >= 1.2.10
        info = all_screens[screen]
        self.fullresolution = '{}x{}'.format(info.width, info.height)

    def __get_screen_number__(self):
        tokens = self.get_dosbox_fullscreenmode().split()
        screen = '0'
        if tokens == [] or tokens[0] != 'screen':
            log_err('unknown option value:', tokens[0])
        if len(tokens) >= 2 and tokens[0] == 'screen':
            screen = tokens[1]
        screen = os.environ.get('SDL_VIDEO_FULLSCREEN_HEAD', screen)
        screen = os.environ.get('SDL_VIDEO_FULLSCREEN_DISPLAY', screen)
        screen = os.environ.get('SDOS_SCREEN', screen)
        screen = os.environ.get('BOXTRON_SCREEN', screen)
        return screen

    def get_bool(self, section, val, default):
        return self.store.getboolean(section, val, fallback=default)

    def get_str(self, section, val, default):
        return self.store.get(section, val, fallback=default)

    def get_confgen_force(self):
        return self.get_bool('confgen', 'force', DEFAULT_CONFGEN_FORCE)

    def get_midi_on(self):
        if enabled_in_env('BOXTRON_NO_MIDI', 'SDOS_NO_MIDI'):
            return False
        return self.get_bool('midi', 'enable', DEFAULT_MIDI_ENABLE)

    def get_midi_tool(self):
        return self.get_str('midi', 'synthesiser', DEFAULT_MIDI_TOOL)

    def set_midi_on(self, value):
        self.store.set('midi', 'enable', str(value))

    def get_midi_soundfont(self):
        assert self.finalized
        return self.get_str('midi', 'soundfont', DEFAULT_SOUNDFONT)

    def get_midi_sequencer(self):
        seq = self.get_str('midi', 'use_sequencer', DEFAULT_MIDI_SEQ_REGEX)
        seq = os.environ.get('SDOS_USE_MIDI_SEQ', seq).strip()
        seq = seq.strip('\'\"')
        return os.environ.get('BOXTRON_USE_MIDI_SEQ', seq)

    def get_dosbox_cmd(self):
        # dosbox.cmd is new name for dosbox.bin
        dosbox_cmd = self.get_str('dosbox', 'cmd', None)
        dosbox_bin = self.get_str('dosbox', 'bin', DEFAULT_DOSBOX_BINARY)
        if not dosbox_cmd:
            dosbox_cmd = dosbox_bin
        cmd = os.environ.get('SDOS_DOSBOX_CMD', dosbox_cmd)
        cmd = os.environ.get('BOXTRON_DOSBOX_CMD', cmd)
        try:
            split = shlex.split(cmd, comments=True)
            return [os.path.expanduser(s) for s in split]
        except ValueError as err:
            log_err('invalid dosbox.bin value:', err)
            return [DEFAULT_DOSBOX_BINARY]

    def set_dosbox_cmd(self, value):
        self.store.set('dosbox', 'cmd', value)

    def get_dosbox_fullscreenmode(self):
        return self.get_str('dosbox', 'fullscreenmode',
                            DEFAULT_FULLSCREEN_MODE)

    def get_dosbox_fullscreen_on(self):
        assert self.finalized
        user_choice = self.get_dosbox_fullscreenmode()
        return 'false' if user_choice == 'disabled' else 'true'

    def get_dosbox_fullresolution(self):
        assert self.finalized
        return self.fullresolution

    def get_dosbox_scaler(self):
        return self.get_str('dosbox', 'scaler', DEFAULT_SCALER)

    def __assure_sf2_exists__(self):
        sf2 = self.get_str('midi', 'soundfont', DEFAULT_SOUNDFONT)
        data_dirs = [os.path.join(self.distdir, 'share')] + xdg.get_data_dirs()
        use_sf2 = ''
        sf2_paths = (os.path.join(d, s, n) for n, d, s in itertools.product(
            [sf2, DEFAULT_SOUNDFONT] + BACKUP_SOUNDFONTS + ['default.sf2'],
            data_dirs,
            ['sounds/sf2', 'soundfonts'],
        ))
        for sf2_path in sf2_paths:
            log('looking for sf2 file:', sf2_path)
            if os.path.isfile(sf2_path):
                use_sf2 = sf2_path
                log('found soundfont:', sf2_path)
                break
        if not use_sf2:
            log_warn('no soundfont found')
            self.store.set('midi', 'soundfont', '')
            return
        _, found_file = os.path.split(use_sf2)
        if found_file != sf2:
            log_warn(sf2, 'soundfont not found. Using', found_file, 'instead.')
        self.store.set('midi', 'soundfont', use_sf2)


def init_settings_file():
    os.makedirs(xdg.CONF_HOME, exist_ok=True)
    old_settings_file = os.path.join(xdg.CONF_HOME, 'steam-dos.conf')
    old_file_exists = os.path.isfile(old_settings_file)
    new_file_exists = os.path.isfile(SETTINGS_FILE)

    # Upgrade old configuration name to boxtron.conf
    #
    # I could simply move the file, but we have opportunity to
    # upgrade documentation in .conf file for all users that tried
    # older versions.
    #
    # TODO drop this code for 1.0.0 release
    #
    if old_file_exists and not new_file_exists:
        old = Settings(conf=old_settings_file)
        old_midi_enable = old.get_bool('midi', 'enable', DEFAULT_MIDI_ENABLE)
        old_midi_sf = old.get_str('midi', 'soundfont', DEFAULT_SOUNDFONT)
        old_bin = old.get_str('dosbox', 'bin', None)
        old_cmd = old.get_str('dosbox', 'cmd', old_bin)
        old_cmd_line = '# cmd = ~/projects/dosbox/src/dosbox'
        if old_cmd and old_cmd != 'dosbox':
            old_cmd_line = 'cmd = {}'.format(old_cmd)
        content = DEFAULT_SETTINGS.format(
            confgen_force=str(old.get_confgen_force()).lower(),
            midi_enable=str(old_midi_enable).lower(),
            midi_tool=old.get_midi_tool(),
            midi_soundfont=old_midi_sf,
            fullscreen_mode=old.get_dosbox_fullscreenmode(),
            scaler=old.get_dosbox_scaler(),
            cmd_example=old_cmd_line)
        with open(SETTINGS_FILE, 'w') as file:
            file.write(content.lstrip())
        os.remove(old_settings_file)
        return

    if not new_file_exists:
        content = DEFAULT_SETTINGS.format(
            confgen_force=str(DEFAULT_CONFGEN_FORCE).lower(),
            midi_enable=str(DEFAULT_MIDI_ENABLE).lower(),
            midi_tool=DEFAULT_MIDI_TOOL,
            midi_soundfont=DEFAULT_SOUNDFONT,
            fullscreen_mode=DEFAULT_FULLSCREEN_MODE,
            scaler=DEFAULT_SCALER,
            cmd_example='# cmd = ~/projects/dosbox/src/dosbox')
        with open(SETTINGS_FILE, 'w') as file:
            file.write(content.lstrip())


init_settings_file()

SETTINGS = Settings()
