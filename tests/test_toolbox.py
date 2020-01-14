#!/usr/bin/python3

# Copyright (C) 2019-2020  Patryk Obara <patryk.obara@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import os
import unittest

import toolbox


class TestWhich(unittest.TestCase):

    def test_python3(self):
        self.assertIsNotNone(toolbox.which('python3'))

    def test_missing_cmd(self):
        self.assertIsNone(toolbox.which('fOoBaRbAz'))


class TestBatchFileDetection(unittest.TestCase):

    def setUp(self):
        self.original_dir = os.getcwd()

    def tearDown(self):
        os.chdir(self.original_dir)

    def test_missing_file(self):
        os.chdir('tests/files/bat/doom2')
        self.assertFalse(toolbox.is_trivial_batch('I_do_not_exist.bat'))

    def test_different_extension(self):
        os.chdir('tests/files/no_conf')
        self.assertFalse(toolbox.is_trivial_batch('file.exe'))

    def test_doom2_1(self):
        os.chdir('tests/files/bat/doom2')
        self.assertTrue(toolbox.is_trivial_batch('doom2.bat'))

    def test_doom2_2(self):
        os.chdir('tests/files/bat/doom2')
        self.assertTrue(toolbox.is_trivial_batch('doom2 + mouse.bat'))

    def test_worms(self):
        os.chdir('tests/files/bat/worms')
        self.assertTrue(toolbox.is_trivial_batch('runworms.bat'))
        path, args = toolbox.read_trivial_batch('runworms.bat')
        self.assertIsNone(path)
        self.assertEqual(args, [r'.\drivec\goworms.bat',
                                '-conf', r'.\worms.conf',
                                '-fullscreen',
                                '-exit'])

    def test_jagged_alliance(self):
        os.chdir('tests/files/bat/jagged-alliance')
        self.assertTrue(toolbox.is_trivial_batch('run.bat'))
        path, args = toolbox.read_trivial_batch('run.bat')
        self.assertIsNone(path)
        self.assertEqual(args, ['-c', 'MOUNT c Installed',
                                '-c', 'IMGMOUNT d cd.iso -t cdrom',
                                '-c', 'c:',
                                '-c', 'cd jagged',
                                '-c', 'ja.bat',
                                '-c', 'exit'])

    def test_stargunner(self):
        os.chdir('tests/files/bat/stargunner')
        self.assertFalse(toolbox.is_trivial_batch('Stargunner.bat'))

    def test_larry7_1(self):
        os.chdir('tests/files/bat/larry7')
        self.assertTrue(toolbox.is_trivial_batch('run.bat'))
        path, args = toolbox.read_trivial_batch('run.bat')
        self.assertEqual(path, 'DOSBOX')
        self.assertEqual(args, ['-conf', r'..\lsl7.conf',
                                '-c', 'exit'])

    def disabled_test_larry7_2(self):
        os.chdir('tests/files/bat')
        self.assertTrue(toolbox.is_trivial_batch('larry7/run.bat'))
        path, args = toolbox.read_trivial_batch('larry7/run.bat')
        self.assertEqual(path, 'larry7/DOSBOX')
        self.assertEqual(args, ['-conf', r'..\lsl7.conf',
                                '-c', 'exit'])

    def test_apogee_throwback_pack(self):
        os.chdir('tests/files/bat/apogee_throwback_pack')
        self.assertTrue(toolbox.is_trivial_batch('Rise of the Triad.bat'))
        path, args = toolbox.read_trivial_batch('Rise of the Triad.bat')
        self.assertEqual(path, 'DOSBOX')
        self.assertEqual(args, ['-conf', 'ROTT.conf', '-noconsole', '-c'])


class TestEnabledInEnv(unittest.TestCase):

    def test_enabled_in_env_on(self):
        self.assertTrue(toolbox.enabled_in_env('HOME'))

    def test_enabled_in_env_off(self):
        self.assertFalse(toolbox.enabled_in_env('THIS_VAR_DOES_NOT_EXIST'))


class TestSed(unittest.TestCase):

    def setUp(self):
        self.test_file = 'tests/files/resource/for_sed'
        with open(self.test_file, 'w') as txt:
            txt.write('foo\nbar\n')

    def tearDown(self):
        os.remove(self.test_file)

    def test_sed(self):
        self.assertEqual(toolbox.get_lines(self.test_file), ['foo\n', 'bar\n'])
        toolbox.sed(self.test_file, r'bar', r'BAR')
        self.assertEqual(toolbox.get_lines(self.test_file), ['foo\n', 'BAR\n'])
        toolbox.sed(self.test_file, r'BAR', r'bar')
        self.assertEqual(toolbox.get_lines(self.test_file), ['foo\n', 'bar\n'])


class TestRpatch(unittest.TestCase):

    def setUp(self):
        self.test_file_1 = 'tests/files/resource/for_rpatch_1'
        self.test_file_2 = 'tests/files/resource/subdir/for_rpatch_2'
        with open(self.test_file_1, 'w') as txt:
            txt.write('abc\ndef\nghi\n')
        with open(self.test_file_2, 'w') as txt:
            txt.write('123\ndef\n789\nabc\n')

    def tearDown(self):
        os.remove(self.test_file_1)
        os.remove(self.test_file_2)

    def test_rpatch_1(self):
        rpatch = [
            r'file:{}'.format(self.test_file_1),
            r's:/def/DEF/',
            r's:|gh|xy|',
            r'file:{}'.format(self.test_file_2),
            r's:/1/x/',
            r's:/2/yy/',
            r's:/9/zzz/',
            r's:/(def)/\1\1/',
            r's:/(a)(b)c/\g<2>0\g<1>0/',
            ''
        ]
        toolbox.apply_resource_patch(rpatch)
        self.assertEqual(toolbox.get_lines(self.test_file_1),
                         ['abc\n', 'DEF\n', 'xyi\n'])
        self.assertEqual(toolbox.get_lines(self.test_file_2),
                         ['xyy3\n', 'defdef\n', '78zzz\n', 'b0a0\n'])

    def test_rpatch_missing_file(self):
        missing_file = 'tests/files/resource/missing_file'
        self.assertFalse(os.path.isfile(missing_file))
        rpatch = [
            r'# existing file should be modified',
            r'file:{}'.format(self.test_file_1),
            r's:/def/DEF/',
            r'# missing file is quietly ignored',
            r'file:{}'.format(missing_file),
            r's:/abc/ABC/',
        ]
        toolbox.apply_resource_patch(rpatch)
        self.assertEqual(toolbox.get_lines(self.test_file_1),
                         ['abc\n', 'DEF\n', 'ghi\n'])
        self.assertFalse(os.path.isfile(missing_file))


class TestGuessInstallDir(unittest.TestCase):

    def test_guess_1(self):
        pfx = '/home/dreamer_/.local/share/'
        cwd = pfx + 'Steam/steamapps/common/Ultimate Doom'
        exp = pfx + r'Steam/steamapps/common/Ultimate\ Doom'
        self.assertEqual(toolbox.guess_game_install_dir(cwd), exp)

    def test_guess_2(self):
        pfx = '/home/dreamer_/.local/share/'
        cwd = pfx + 'Steam/SteamApps/common/Ultimate Doom/base'
        exp = pfx + r'Steam/SteamApps/common/Ultimate\ Doom'
        self.assertEqual(toolbox.guess_game_install_dir(cwd), exp)

    def test_guess_3(self):
        pfx = '/mnt/steam-lib/steamapps/common/'
        cwd = pfx + 'Heroes of Might & Magic III - HD Edition/data'
        exp = pfx + r'Heroes\ of\ Might\ \&\ Magic\ III\ -\ HD\ Edition'
        self.assertEqual(toolbox.guess_game_install_dir(cwd), exp)

    def test_guess_4(self):
        cwd = '/mnt/steam-lib/steamapps/common/'
        self.assertEqual(toolbox.guess_game_install_dir(cwd), None)


class TestPidfile(unittest.TestCase):

    def test_file_created(self):
        pidf_path = 'tests/files/pid_file'
        self.assertFalse(os.path.isfile(pidf_path))
        with toolbox.PidFile(pidf_path):
            self.assertTrue(os.path.isfile(pidf_path))
        self.assertFalse(os.path.isfile(pidf_path))


class TestBatchVariables(unittest.TestCase):

    def test_guess_relative_path_1(self):
        dp0 = toolbox.relative_path_to('/home/user', '/home/user/file')
        self.assertEqual(dp0, './')

    def test_guess_relative_path_2(self):
        dp0 = toolbox.relative_path_to('/home/user', '/home/user/dir/file')
        self.assertEqual(dp0, './dir/')

    def test_guess_relative_path_3(self):
        dp0 = toolbox.relative_path_to('/home/user', '/home/user/dir/file')
        self.assertEqual(dp0, './dir/')

    def test_guess_relative_path_4(self):
        dp0 = toolbox.relative_path_to('/home/user/dir_a',
                                       '/home/user/dir_b/file')
        self.assertEqual(dp0, './../dir_b/')

    def test_guess_relative_path_5(self):
        dp0 = toolbox.relative_path_to('/home/user/dir_a/foo',
                                       '/home/user/dir_b/file')
        self.assertEqual(dp0, './../../dir_b/')

    def test_guess_relative_path_6(self):
        dp0 = toolbox.relative_path_to('/home/user/foo',
                                       '/home/user/bar/file')
        self.assertEqual(dp0, './../bar/')


class TestHashing(unittest.TestCase):

    def test_sha256sum(self):
        val = toolbox.sha256sum('tests/files/default/dosbox.conf')
        exp = '9e6d9ab036ba68257a6d70f11265cdb304b9c1054363c0537755a957c8d57c32'
        self.assertEqual(val, exp)


class TestGameId(unittest.TestCase):

    def tearDown(self):
        os.environ.pop('SteamAppId', None)
        os.environ.pop('SteamGameId', None)
        os.environ.pop('GOG_GAME_ID', None)

    def test_defaults(self):
        os.environ.pop('SteamAppId', None)
        os.environ.pop('SteamGameId', None)
        os.environ.pop('GOG_GAME_ID', None)
        self.assertEqual('0', toolbox.get_game_install_id())
        self.assertIsNone(toolbox.get_game_global_id())

    def test_install_id_steam_game(self):
        os.environ['SteamAppId'] = '12340'
        os.environ['SteamGameId'] = '12340'
        self.assertEqual('12340', toolbox.get_game_install_id())

    def test_global_id_steam_game(self):
        os.environ['SteamAppId'] = '12340'
        os.environ['SteamGameId'] = '12340'
        self.assertEqual('steam:12340', toolbox.get_game_global_id())

    def test_install_id_non_steam_game(self):
        os.environ['SteamAppId'] = '0'
        os.environ['SteamGameId'] = '123456789'
        self.assertEqual('123456789', toolbox.get_game_install_id())

    def test_global_id_non_steam_game(self):
        os.environ['SteamAppId'] = '0'
        os.environ['SteamGameId'] = '123456789'
        self.assertIsNone(toolbox.get_game_global_id())

    def test_install_id_gog(self):
        os.environ['GOG_GAME_ID'] = '9090909'
        self.assertEqual('9090909', toolbox.get_game_install_id())

    def test_global_id_gog(self):
        os.environ['GOG_GAME_ID'] = '9090909'
        self.assertEqual('gog:9090909', toolbox.get_game_global_id())


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
