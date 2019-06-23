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


def get_lines(txt_file):
    with open(txt_file) as tfile:
        return tfile.readlines()


class TestSed(unittest.TestCase):

    def test_sed(self):
        test_file = 'tests/files/resource/for_sed'
        self.assertEqual(get_lines(test_file), ['foo\n', 'bar\n', 'baz\n'])
        toolbox.sed(test_file, r'bar', r'BAR')
        self.assertEqual(get_lines(test_file), ['foo\n', 'BAR\n', 'baz\n'])
        toolbox.sed(test_file, r'BAR', r'bar')
        self.assertEqual(get_lines(test_file), ['foo\n', 'bar\n', 'baz\n'])


class TestPidfile(unittest.TestCase):

    def test_file_created(self):
        pidf_path = 'tests/files/pid_file'
        self.assertFalse(os.path.isfile(pidf_path))
        with toolbox.PidFile(pidf_path):
            self.assertTrue(os.path.isfile(pidf_path))
        self.assertFalse(os.path.isfile(pidf_path))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
