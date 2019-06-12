#!/usr/bin/env python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import unittest

import fsl


class TestLauncherParser(unittest.TestCase):

    def test_parser_gk1(self):
        path = 'tests/files/sierra/gabriel_knight/'
        ini = path + 'SierraLauncher.ini'
        launcher = fsl.SierraLauncherConfig(ini_file=ini)
        self.assertEqual(launcher.name,
                         'Gabriel Knight - Sins of the Fathers')
        self.assertEqual(launcher.games_number(), 1)
        game = launcher.games[0]
        self.assertEqual(game['path'], path + 'GK1/DOSBOX')
        self.assertEqual(game['args'], ['-conf', 'dosboxGK.conf',
                                        '-conf', 'dosboxGK_single.conf',
                                        '-noconsole',
                                        '-c', 'exit'])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()