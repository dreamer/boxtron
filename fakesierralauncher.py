#!/usr/bin/python3

# Copyright (C) 2019-2020  Patryk Obara <patryk.obara@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Fake Sierra Launcher
"""

import configparser
import os

from log import log_warn, log_err
from toolbox import argsplit_windows
from winpathlib import to_posix_path

SIERRA_GAME = os.environ.get('BOXTRON_SIERRA_GAME') or \
              os.environ.get('SDOS_SIERRA_GAME', '1')


class SierraLauncherConfig:
    """Interpret Sierra Launcher configuration file.

    Usually this file is called SierraLauncher.ini and is located in top
    level of game installation directory.
    """

    def __init__(self, *, ini_file):
        assert ini_file
        self.name = ''
        self.games = {}
        self.games_num = 0
        self.selected_game = 0
        path, _ = os.path.split(ini_file)
        self.__parse_config__(ini_file, path)
        self.select_game()

    def games_number(self):
        """Return number of games defined in the launcher."""
        return self.games_num

    def select_game(self):
        """Select game in collection."""
        index = 0
        try:
            index = int(SIERRA_GAME) - 1
        except ValueError:
            log_warn('BOXTRON_SIERRA_GAME must be a numerical value')
        self.selected_game = min(max(0, index), self.games_num - 1)
        if self.selected_game != index:
            log_warn('game', SIERRA_GAME, 'not found.')
            log_warn('This collection defines games',
                     '1..' + str(self.games_num))
            self.selected_game = 0

    def __parse_config__(self, ini_file, ini_dir):
        config = configparser.ConfigParser(delimiters='=')
        config.read(ini_file)
        assert config.has_section('Launcher'), 'Unknown file format'
        launcher = config['Launcher']
        self.name = launcher['name']
        self.games_num = int(launcher['numbuttons'])
        for i in range(0, self.games_num):
            self.__parse_game_entry__(launcher, ini_dir, i)

    def __parse_game_entry__(self, launcher, ini_dir, i):
        num = i + 1
        name = launcher['game%dname' % num]
        prog = launcher['game%dprog' % num]
        path = launcher['game%dpath' % num]
        exe = launcher['game%dexe' % num]
        cmd = launcher['game%dcmd' % num]
        self.games[i] = {'name': name}
        game = self.games[i]
        orig_cwd = os.getcwd()
        os.chdir(ini_dir)
        real_path = to_posix_path(path)
        if real_path:
            game['path'] = os.path.join(ini_dir, real_path)
        else:
            log_err("can't find path", path)
            game['path'] = orig_cwd
        if prog.lower() == 'dosbox':  # used only in Legacy launcher
            game['args'] = ['-c', 'mount C .',
                            '-c', 'C:',
                            '-c', exe,
                            '-c', 'exit']  # yapf: disable
        else:  # usually 'other', most common option
            game['args'] = argsplit_windows(cmd)
        os.chdir(orig_cwd)

    def chdir(self):
        """Change working directory to the one defined for game game_num."""
        assert self.selected_game < self.games_number()
        path = self.games[self.selected_game]['path']
        os.chdir(path)

    def get_name(self):
        """Return name of the selected game."""
        assert self.selected_game < self.games_number()
        return self.games[self.selected_game]['name']

    def get_args(self):
        """Return dosbox arguments to run the selected game."""
        assert self.selected_game < self.games_number()
        return self.games[self.selected_game]['args']
