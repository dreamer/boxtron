#!/usr/bin/env python3

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
        args = toolbox.read_trivial_batch('runworms.bat')
        self.assertEqual(args, [r'.\drivec\goworms.bat',
                                '-conf', r'.\worms.conf',
                                '-fullscreen',
                                '-exit'])

    def test_jagged_alliance(self):
        os.chdir('tests/files/bat/jagged-alliance')
        self.assertTrue(toolbox.is_trivial_batch('run.bat'))
        args = toolbox.read_trivial_batch('run.bat')
        self.assertEqual(args, ['-c', 'MOUNT c Installed',
                                '-c', 'IMGMOUNT d cd.iso -t cdrom',
                                '-c', 'c:',
                                '-c', 'cd jagged',
                                '-c', 'ja.bat',
                                '-c', 'exit'])

    def test_stargunner(self):
        os.chdir('tests/files/bat/stargunner')
        self.assertFalse(toolbox.is_trivial_batch('Stargunner.bat'))


class TestEnabledInEnv(unittest.TestCase):

    def test_enabled_in_env_on(self):
        self.assertTrue(toolbox.enabled_in_env('HOME'))

    def test_enabled_in_env_off(self):
        self.assertFalse(toolbox.enabled_in_env('THIS_VAR_DOES_NOT_EXIST'))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
