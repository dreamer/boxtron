#!/usr/bin/python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import os
import unittest

import cuescanner


class TestCueScanner(unittest.TestCase):

    def setUp(self):
        self.original_dir = os.getcwd()

    def tearDown(self):
        os.chdir(self.original_dir)

    def test_is_cue_1(self):
        os.chdir('tests/files/cue')
        self.assertFalse(cuescanner.is_cue_file('empty_file.cue'))
        self.assertFalse(cuescanner.is_cue_file('descent2'))
        self.assertFalse(cuescanner.is_cue_file('some_text_file'))

    def test_is_cue_2(self):
        os.chdir('tests/files/cue')
        self.assertTrue(cuescanner.is_cue_file('descent2/descent_ii.inst'))
        self.assertTrue(cuescanner.is_cue_file('tr1/GAME.DAT'))
        self.assertTrue(cuescanner.is_cue_file('worms/worms.cue'))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
