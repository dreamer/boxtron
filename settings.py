#!/usr/bin/env python3

# pylint: disable=missing-docstring

"""
Settings file creation and handling.
"""

import configparser
import os

from toolbox import print_err
from toolbox import enabled_in_env


CONF_HOME = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.expanduser('~/.config')

DATA_HOME = os.environ.get('XDG_DATA_HOME') or \
            os.path.expanduser('~/.local/share')

SETTINGS_FILE = os.path.join(CONF_HOME, 'steam-dos.conf')

DEFAULT_CONFGEN_FORCE = False

DEFAULT_MIDI_ENABLE = True

DEFAULT_MIDI_SOUNDFONT = 'FluidR3_GM.sf2'

DEFAULT_SETTINGS = f"""
[confgen]
# Set this value to 'true' if you want steam-dos to re-create
# DOSBox configuration on every run.
force = {str(DEFAULT_CONFGEN_FORCE).lower()}

[midi]
# You can disable MIDI support here.
enable = {str(DEFAULT_MIDI_ENABLE).lower()}

# steam-dos will look for a soundfont in following directories:
# /usr/share/soundfonts/
# /usr/share/sounds/sf2/
# /usr/local/share/soundfonts/
# /usr/local/share/sounds/sf2/
# ~/.local/share/sounds/sf2/  (or wherever XDG_DATA_HOME points)
# ~/.local/share/soundfonts/  (or wherever XDG_DATA_HOME points)
soundfont = {DEFAULT_MIDI_SOUNDFONT}
""".lstrip()


class Settings():

    def __init__(self):
        self.store = configparser.ConfigParser()
        self.store.read(SETTINGS_FILE)
        midi_on = self.get_midi_on()
        if midi_on:
            self.__assure_sf2_exists__()

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

    def get_midi_soundfont(self):
        return self.__get_str__('midi', 'soundfont', DEFAULT_MIDI_SOUNDFONT)

    def __assure_sf2_exists__(self):
        sf2 = self.get_midi_soundfont()
        sf2_search = [
            ['/usr/share/sounds/sf2'],
            ['/usr/share/soundfonts'],
            ['/usr/local/share/sounds/sf2'],
            ['/usr/local/share/soundfonts'],
            [DATA_HOME, 'sounds/sf2'],
            [DATA_HOME, 'soundfonts'],
        ]
        selected = ''
        default = ''
        os_default = ''
        for path in sf2_search:
            selected_path = os.path.join(*path, sf2)
            default1_path = os.path.join(*path, DEFAULT_MIDI_SOUNDFONT)
            default2_path = os.path.join(*path, 'default.sf2z')
            if os.path.isfile(selected_path):
                selected = selected_path
            if os.path.isfile(default1_path):
                default = default1_path
            if os.path.isfile(default2_path):
                os_default = default2_path
        use_sf2 = selected or default or os_default
        if not use_sf2:
            print_err('steam-dos: warning: Not suitable soundfont found.',
                      'Disabling MIDI support.')
            self.store.set('midi', 'enable', 'False')
            return
        _, found_file = os.path.split(use_sf2)
        if found_file != sf2:
            print_err(f'steam-dos: warning: {sf2} soundfont not found.',
                      f'Using {found_file} instead.')
        self.store.set('midi', 'soundfont', use_sf2)


os.makedirs(CONF_HOME, exist_ok=True)
if not os.path.isfile(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'w') as file:
        file.write(DEFAULT_SETTINGS)

SETTINGS = Settings()
