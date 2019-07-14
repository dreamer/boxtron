#!/usr/bin/python3

# pylint: disable=missing-docstring

"""
Settings file creation and handling.
"""

import configparser
import os
import shlex

import xdg
import xlib

from toolbox import print_err
from toolbox import enabled_in_env

SETTINGS_FILE = os.path.join(xdg.CONF_HOME, 'steam-dos.conf')

DEFAULT_CONFGEN_FORCE = False

DEFAULT_MIDI_ENABLE = True

DEFAULT_MIDI_TOOL = 'timidity'

DEFAULT_MIDI_SOUNDFONT = 'FluidR3_GM.sf2'

DEFAULT_DOSBOX_BINARY = 'dosbox'

DEFAULT_FULLSCREEN_MODE = 'screen 0'

DEFAULT_SCALER = 'normal3x'

DEFAULT_SETTINGS = """
[confgen]
# Set this value to 'true' if you want steam-dos to re-create DOSBox
# configuration on every run.
force = {confgen_force}

[midi]
# You can disable MIDI support here.
enable = {midi_enable}

# Select preferred software synthesiser here.
# Can be either 'timidity' or 'fluidsynth'
synthesiser = {midi_tool}

# steam-dos will look for a soundfont in following directories:
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
#   Default is '{fullscreen_mode}', which is your primary display.
#   You can override this selection per-game with SDOS_SCREEN environment
#   variable, e.g: 'SDOS_SCREEN=2 %command%'
# - desktop:
#   The whole desktop area will be used (all displays) with the game centred,
#   the native resolution of your displays will be preserved.
fullscreenmode = {fullscreen_mode}

# Pick the default scaler, that you want to use for all games.
# You can override selection per-game by changing option render.scaler in file
# steam_dos_<appid>_<id>.conf in game's installation dir.
# Here's comparison of different scalers: https://www.dosbox.com/wiki/Scaler
scaler = {scaler}

# Uncomment following line to specify a different DOSBox build:
# cmd = ~/projects/dosbox/src/dosbox
""".format(confgen_force=str(DEFAULT_CONFGEN_FORCE).lower(),
           midi_enable=str(DEFAULT_MIDI_ENABLE).lower(),
           midi_tool=DEFAULT_MIDI_TOOL,
           midi_soundfont=DEFAULT_MIDI_SOUNDFONT,
           fullscreen_mode=DEFAULT_FULLSCREEN_MODE,
           scaler=DEFAULT_SCALER).lstrip()


class Settings():

    def __init__(self):
        self.store = configparser.ConfigParser(interpolation=None)
        self.store.add_section('confgen')
        self.store.add_section('midi')
        self.store.add_section('dosbox')
        self.store.read(SETTINGS_FILE)
        self.fullresolution = 'desktop'
        self.finalized = False
        self.distdir = os.path.dirname(os.path.abspath(__file__))

    def setup(self):
        """Finalize settings initialization on request.

        Some settings need more involved initialization/detection procedure,
        which might fail or leave extensive logs on stderr.  We want this
        part of settings initialization only when actually needed.
        """
        midi_on = self.get_midi_on()
        if midi_on:
            self.__assure_sf2_exists__()
        self.__setup_fullscreen__()
        self.finalized = True

    def __setup_fullscreen__(self):
        user_choice = self.get_dosbox_fullscreenmode()
        env_override = 'SDOS_SCREEN' in os.environ or \
                       'SDL_VIDEO_FULLSCREEN_DISPLAY' in os.environ or \
                       'SDL_VIDEO_FULLSCREEN_HEAD' in os.environ

        if user_choice == 'desktop' and not env_override:
            return

        screen = self.__get_screen_number__()
        all_screens = xlib.query_screens()

        if all_screens == {}:
            print_err('steam-dos: error: no screens detected')
        for number, info in all_screens.items():
            print_err("steam-dos: screen '{}': {}x{}".format(
                number, info.width, info.height))

        if screen not in all_screens:
            print_err("steam-dos: screen '{}' not found".format(screen))
            if '0' in all_screens:
                screen = '0'
                print_err("steam-dos: using '" + screen + "' instead")
            else:
                print_err("steam-dos: using desktop as screen instead")
                return

        print_err("steam-dos: selected screen '{}'".format(screen))
        os.putenv('SDL_VIDEO_FULLSCREEN_DISPLAY', screen)  # SDL >= 1.2.14
        os.putenv('SDL_VIDEO_FULLSCREEN_HEAD', screen)  # SDL >= 1.2.10
        info = all_screens[screen]
        self.fullresolution = '{}x{}'.format(info.width, info.height)

    def __get_screen_number__(self):
        tokens = self.get_dosbox_fullscreenmode().split()
        screen = '0'
        if tokens == [] or tokens[0] != 'screen':
            print_err('steam-dos: error: unknown option value:', tokens[0])
        if len(tokens) >= 2 and tokens[0] == 'screen':
            screen = tokens[1]
        screen = os.environ.get('SDL_VIDEO_FULLSCREEN_HEAD', screen)
        screen = os.environ.get('SDL_VIDEO_FULLSCREEN_DISPLAY', screen)
        screen = os.environ.get('SDOS_SCREEN', screen)
        return screen

    def __get_bool__(self, section, val, default):
        return self.store.getboolean(section, val, fallback=default)

    def __get_str__(self, section, val, default):
        return self.store.get(section, val, fallback=default)

    def get_confgen_force(self):
        return self.__get_bool__('confgen', 'force', DEFAULT_CONFGEN_FORCE)

    def get_midi_on(self):
        if enabled_in_env('SDOS_NO_MIDI'):
            return False
        return self.__get_bool__('midi', 'enable', DEFAULT_MIDI_ENABLE)

    def get_midi_tool(self):
        return self.__get_str__('midi', 'synthesiser', DEFAULT_MIDI_TOOL)

    def set_midi_on(self, value):
        self.store.set('midi', 'enable', str(value))

    def get_midi_soundfont(self):
        assert self.finalized
        return self.__get_str__('midi', 'soundfont', DEFAULT_MIDI_SOUNDFONT)

    def get_dosbox_cmd(self):
        # dosbox.cmd is new name for dosbox.bin
        dosbox_cmd = self.__get_str__('dosbox', 'cmd', None)
        dosbox_bin = self.__get_str__('dosbox', 'bin', DEFAULT_DOSBOX_BINARY)
        if not dosbox_cmd:
            dosbox_cmd = dosbox_bin
        cmd = os.environ.get('SDOS_DOSBOX_CMD', dosbox_cmd)
        try:
            split = shlex.split(cmd, comments=True)
            return [os.path.expanduser(s) for s in split]
        except ValueError as err:
            print_err('steam-dos: error: invalid dosbox.bin value:', err)
            return [DEFAULT_DOSBOX_BINARY]

    def set_dosbox_cmd(self, value):
        self.store.set('dosbox', 'cmd', value)

    def get_dosbox_fullscreenmode(self):
        return self.__get_str__('dosbox', 'fullscreenmode',
                                DEFAULT_FULLSCREEN_MODE)

    def get_dosbox_fullresolution(self):
        assert self.finalized
        return self.fullresolution

    def get_dosbox_scaler(self):
        return self.__get_str__('dosbox', 'scaler', DEFAULT_SCALER)

    def __assure_sf2_exists__(self):
        sf2 = self.__get_str__('midi', 'soundfont', DEFAULT_MIDI_SOUNDFONT)
        sf2_search = [
            ['/usr/share/sounds/sf2'],
            ['/usr/share/soundfonts'],
            ['/usr/local/share/sounds/sf2'],
            ['/usr/local/share/soundfonts'],
            [xdg.DATA_HOME, 'sounds/sf2'],
            [xdg.DATA_HOME, 'soundfonts'],
            [self.distdir, 'share/sounds/sf2'],
            [self.distdir, 'share/soundfonts'],
        ]
        selected = ''
        default = ''
        os_default = ''
        for path in sf2_search:
            # TODO avoid unnecessary list append after Python 3.5 is dropped
            selected_path = os.path.join(*(path + [sf2]))
            default1_path = os.path.join(*(path + [DEFAULT_MIDI_SOUNDFONT]))
            default2_path = os.path.join(*(path + ['default.sf2']))
            if os.path.isfile(selected_path):
                selected = selected_path
            if os.path.isfile(default1_path):
                default = default1_path
            if os.path.isfile(default2_path):
                os_default = default2_path
        use_sf2 = selected or default or os_default
        if not use_sf2:
            print_err('steam-dos: warning: No suitable soundfont found.',
                      'Disabling MIDI support.')
            self.store.set('midi', 'enable', 'False')
            return
        _, found_file = os.path.split(use_sf2)
        if found_file != sf2:
            print_err(('steam-dos: warning: {0} soundfont not found. '
                       'Using {1} instead.').format(sf2, found_file))
        self.store.set('midi', 'soundfont', use_sf2)


os.makedirs(xdg.CONF_HOME, exist_ok=True)
if not os.path.isfile(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'w') as file:
        file.write(DEFAULT_SETTINGS)

SETTINGS = Settings()
