#!/usr/bin/env python3

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


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
