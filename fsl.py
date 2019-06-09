#!/usr/bin/env python3

"""
Fake Sierra Launcher
"""

import configparser
import os

from toolbox import argsplit_windows
from winpathlib import to_posix_path


class SierraLauncherConfig:
    """Interpret Sierra Launcher configuration file.

    Usually this file is called SierraLauncher.ini and is located in top
    level of game installation directory.
    """

    def __init__(self, *, ini_file):
        self.name = ''
        self.games = {}
        self.games_num = 0
        ini_file = to_posix_path(ini_file)
        path, _ = os.path.split(ini_file)
        self.__parse_config__(ini_file, path)

    def games_number(self):
        """Return number of games defined in the launcher."""
        return self.games_num

    def __parse_config__(self, ini_file, ini_dir):
        config = configparser.ConfigParser(delimiters='=')
        config.read(ini_file)
        assert config.has_section('Launcher'), 'Unknown file format'
        launcher = config['Launcher']
        self.name = launcher['name']
        self.games_num = int(launcher['numbuttons'])
        for i in range(0, self.games_num):
            path = launcher['game{}path'.format(i + 1)]
            exe = launcher['game{}exe'.format(i + 1)]
            args = launcher['game{}cmd'.format(i + 1)]
            exe_path = to_posix_path(os.path.join(ini_dir, path, exe))
            real_path, real_exe = os.path.split(exe_path)
            self.games[i] = {
                'path': real_path,
                'exe': real_exe,
                'args': argsplit_windows(args),
            }

    def chdir(self, game_num):
        """Change working directory to the one defined for game game_num."""
        assert game_num < self.games_number()
        path = self.games[game_num]['path']
        os.chdir(path)
