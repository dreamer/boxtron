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

    def test_list_referenced_files_1(self):
        os.chdir('tests/files/cue/descent2')
        found_entries = list(cuescanner.list_file_entries('descent_ii.inst'))
        self.assertEqual(found_entries, [('DESCENT_II.gog', 'BINARY')])

    def test_list_referenced_files_2(self):
        os.chdir('tests/files/cue/tr1')
        found_entries = list(cuescanner.list_file_entries('GAME.DAT'))
        expected = [
            ('GAME.GOG', 'BINARY'),
            ('02.mp3', 'MP3'),
            ('03.mp3', 'MP3'),
            ('04.mp3', 'MP3'),
            ('05.mp3', 'MP3'),
            ('06.mp3', 'MP3'),
            ('07.mp3', 'MP3'),
            ('08.mp3', 'MP3'),
            ('09.mp3', 'MP3'),
            ('10.mp3', 'MP3'),
        ]
        self.assertEqual(expected, found_entries)

    def test_list_referenced_files_3(self):
        os.chdir('tests/files/cue/worms')
        found_entries = list(cuescanner.list_file_entries('worms.cue'))
        expected = [
            ('worms.bin', 'BINARY'),
            ('02.ogg', 'OGG'),
            ('03.ogg', 'OGG'),
            ('04.ogg', 'OGG'),
            ('05.ogg', 'OGG'),
            ('06.ogg', 'OGG'),
            ('07.ogg', 'OGG'),
            ('08.ogg', 'OGG'),
            ('09.ogg', 'OGG'),
            ('10.ogg', 'OGG'),
            ('11.ogg', 'OGG'),
            ('12.ogg', 'OGG'),
            ('13.ogg', 'OGG'),
            ('14.ogg', 'OGG'),
            ('15.ogg', 'OGG'),
            ('16.ogg', 'OGG'),
            ('17.ogg', 'OGG'),
            ('18.ogg', 'OGG'),
        ]
        self.assertEqual(expected, found_entries)

    def test_cue_file_paths_1(self):
        os.chdir('tests/files/cue/descent2')
        self.assertFalse(cuescanner.valid_cue_file_paths('descent_ii.inst'))

    def test_cue_file_paths_2(self):
        os.chdir('tests/files/cue/tr1')
        self.assertTrue(cuescanner.valid_cue_file_paths('GAME.DAT'))

    def test_cue_file_paths_3(self):
        os.chdir('tests/files/cue/worms')
        self.assertTrue(cuescanner.valid_cue_file_paths('worms.cue'))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
