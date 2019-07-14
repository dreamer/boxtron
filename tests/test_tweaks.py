#!/usr/bin/python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import os
import unittest

import tweaks


class TestDosboxConfiguration(unittest.TestCase):

    def test_relative_path(self):
        needed, path = tweaks.check_cwd(['test/files/confs/dosbox/dosbox.exe',
                                         '-conf', '..\\c1.conf'])
        self.assertEqual((needed, path), (False, None))

    # $ (…)/tests/files/confs/dosbox/dosbox.exe -conf test\files\confs\c1.conf
    #
    def test_good_cwd(self):
        conf_file = 'tests/files/confs/c1.conf'
        conf_file_win = conf_file.replace('/', '\\')
        self.assertTrue(os.path.isfile(conf_file))
        exe = os.path.join(os.getcwd(), 'tests/files/confs/dosbox/dosbox.exe')
        needed, path = tweaks.check_cwd([exe, '-conf', conf_file_win])
        self.assertEqual((needed, path), (False, os.getcwd()))

    # Assuming working dir was supposed to be …/confs/dosbox
    #
    # $ pwd
    # <path>
    # $ <path>/tests/files/confs/dosbox/dosbox.exe -conf ..\c1.conf
    #
    def test_bad_cwd_1(self):
        expected_path = 'tests/files/confs/dosbox'
        self.assertFalse(os.getcwd().endswith(expected_path))
        exe = os.path.join(os.getcwd(), 'tests/files/confs/dosbox/dosbox.exe')
        needed, new_path = tweaks.check_cwd([exe, '-conf', '..\\c1.conf'])
        self.assertTrue(needed)
        self.assertEqual(new_path, os.path.join(os.getcwd(), expected_path))

    # Assuming working dir was supposed to be …/confs
    #
    # $ pwd
    # <path>
    # $ <path>/tests/files/confs/dosbox/dosbox.exe -conf c1.conf
    #
    def test_bad_cwd_2(self):
        expected_path = 'tests/files/confs'
        self.assertFalse(os.getcwd().endswith(expected_path))
        exe = os.path.join(os.getcwd(), 'tests/files/confs/dosbox/dosbox.exe')
        needed, new_path = tweaks.check_cwd([exe, '-conf', 'c1.conf'])
        self.assertTrue(needed)
        self.assertEqual(new_path, os.path.join(os.getcwd(), expected_path))

    def test_tweak_command_match(self):
        tweaks.TWEAKS_DB['1'] = {
            'commands': {
                r'.*': {'args': ['-conf', 'new']},
            }
        }
        args = tweaks.tweak_command('1', ['/path/program', '-conf', 'old'])
        self.assertTrue(tweaks.command_tweak_needed('1'))
        self.assertEqual(args, ['-conf', 'new'])

    def test_tweak_command_no_match(self):
        tweaks.TWEAKS_DB['2'] = {
            'commands': {
                r'.*launcher': {'args': ['-conf', 'new']},
            }
        }
        args = tweaks.tweak_command('2', ['/path/program', '-conf', 'old'])
        self.assertTrue(tweaks.command_tweak_needed('2'))
        self.assertEqual(args, ['-conf', 'old'])

    def test_configuration_tweak_1(self):
        self.assertFalse('3' in tweaks.TWEAKS_DB)
        self.assertEqual(tweaks.get_conf_tweak('3'), {})

    def test_configuration_tweak_2(self):
        tweaks.TWEAKS_DB['4'] = {'foo': {}}
        self.assertTrue('4' in tweaks.TWEAKS_DB)
        self.assertEqual(tweaks.get_conf_tweak('4'), {})

    def test_configuration_tweak_3(self):
        conf_tweak = {
            'foo': {'bar': 'baz'}
        }
        tweaks.TWEAKS_DB['5'] = {'conf': conf_tweak}
        self.assertTrue('5' in tweaks.TWEAKS_DB)
        self.assertEqual(tweaks.get_conf_tweak('5'), conf_tweak)

    def test_midi_preset_1(self):
        tweaks.TWEAKS_DB['6'] = {'midi': 'auto'}
        self.assertEqual(tweaks.get_midi_preset('6'), 'auto')

    def test_midi_preset_3(self):
        tweaks.TWEAKS_DB['7'] = {'midi': 'disable'}
        self.assertEqual(tweaks.get_midi_preset('7'), 'disable')

    def test_midi_preset_2(self):
        tweaks.TWEAKS_DB['8'] = {'midi': 'enable'}
        self.assertEqual(tweaks.get_midi_preset('8'), 'enable')

    def test_midi_preset_4(self):
        self.assertFalse('9' in tweaks.TWEAKS_DB)
        self.assertEqual(tweaks.get_midi_preset('9'), 'enable')

    def test_download_tweak_needed(self):
        tweaks.TWEAKS_DB['11'] = { 'download': {} }
        self.assertTrue(tweaks.download_tweak_needed('11'))

    def test_install_tweak_needed(self):
        tweaks.TWEAKS_DB['12'] = { 'install': 'install_test_42' }
        self.assertTrue(tweaks.install_tweak_needed('12'))
        self.assertEqual(tweaks.install('12'), 42)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
