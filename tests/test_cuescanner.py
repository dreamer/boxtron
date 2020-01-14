#!/usr/bin/python3

# Copyright (C) 2019-2020  Patryk Obara <patryk.obara@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import os
import unittest

import cuescanner
import toolbox


def tracks(path_fmt, stated_type, first, last):
    names = [path_fmt.format(i) for i in range(first, last+1)]
    types = [stated_type] * (last + 1 - first)
    return list(zip(names, types))


class TestCueScanner(unittest.TestCase):

    def setUp(self):
        self.test_file_1 = None
        self.original_dir = os.getcwd()

    def tearDown(self):
        if self.test_file_1:
            os.remove(self.test_file_1)
            self.test_file_1 = None
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

    def test_descent_2(self):
        os.chdir('tests/files/cue/descent2')
        self.assertFalse(cuescanner.valid_cue_file_paths('descent_ii.inst'))
        self.assertTrue(cuescanner.valid_indexes('descent_ii.inst'))

    def test_tr1(self):
        os.chdir('tests/files/cue/tr1')
        self.assertTrue(cuescanner.valid_cue_file_paths('GAME.DAT'))
        self.assertFalse(cuescanner.valid_indexes('GAME.DAT'))

    def test_worms(self):
        os.chdir('tests/files/cue/worms')
        self.assertTrue(cuescanner.valid_cue_file_paths('worms.cue'))
        self.assertTrue(cuescanner.valid_indexes('worms.cue'))

    def test_cue_file_correction(self):
        os.chdir('tests/files/cue/descent2')
        self.test_file_1 = 'new.cue'
        self.assertFalse(os.path.isfile(self.test_file_1))
        new = cuescanner.create_fixed_cue_file('descent_ii.inst', 'new.cue')
        self.assertEqual(new, self.test_file_1)
        self.assertTrue(os.path.isfile(self.test_file_1))
        line_0 = toolbox.get_lines('new.cue')[0]
        self.assertEqual('FILE "descent_ii.gog" BINARY\n', line_0)
        self.assertTrue(cuescanner.valid_indexes('new.cue'))

    def test_index_correction(self):
        os.chdir('tests/files/cue/tr1')
        self.test_file_1 = 'new.cue'
        self.assertFalse(os.path.isfile('new.cue'))
        cuescanner.create_fixed_cue_file('GAME.DAT', 'new.cue')
        self.assertTrue(cuescanner.valid_cue_file_paths('new.cue'))
        self.assertTrue(cuescanner.valid_indexes('new.cue'))

    # Tracks in this file exist in relative location, but are mislabeled as MP3
    #
    # Surprisingly, it does not matter to DOSBox - it plays the files anyway
    # It makes problem to DOSBox-X - it is unable to load .cue file from a
    # different location, no matter if paths or types are correct or not.
    #
    def test_gog_mk3_1(self):
        os.chdir('tests/files/cue/mk3/DOSBOX')
        mk3_cue = '../mk3/IMAGE/MK3.cue'
        self.assertTrue(cuescanner.is_cue_file(mk3_cue))
        found_entries = list(cuescanner.list_file_entries(mk3_cue))
        # original file has incorrect file type
        ogg_tracks = tracks('Track{:02d}.ogg', 'MP3', 2, 47)
        expected = [('MK3.GOG', 'BINARY')] + ogg_tracks
        self.assertEqual(expected, found_entries)
        self.assertTrue(cuescanner.valid_cue_file_paths(mk3_cue))
        self.assertTrue(cuescanner.valid_indexes(mk3_cue))

    # Alone in the Dark 1 has audio tracks embedded in the image.
    #
    def test_alone1(self):
        os.chdir('tests/files/cue/alone1/DOSBOX')
        alone1_cue = '../GAME.INST'
        found_entries = list(cuescanner.list_file_entries(alone1_cue))
        expected = [('GAME.GOG', 'BINARY')]
        self.assertEqual(expected, found_entries)
        self.assertTrue(cuescanner.is_cue_file(alone1_cue))
        self.assertTrue(cuescanner.valid_cue_file_paths(alone1_cue))
        self.assertTrue(cuescanner.valid_indexes(alone1_cue))

    # Carmageddon
    #
    def test_carmageddon(self):
        os.chdir('tests/files/cue/carma/DOSBOX')
        cue_file = '../CARMA/GAME.DAT'
        self.assertTrue(cuescanner.is_cue_file(cue_file))
        self.assertFalse(cuescanner.valid_cue_file_paths(cue_file))
        self.assertTrue(cuescanner.valid_indexes(cue_file))
        self.test_file_1 = '../CARMA/new.cue'
        self.assertFalse(os.path.isfile(self.test_file_1))
        new = cuescanner.create_fixed_cue_file('../CARMA/GAME.DAT', 'new.cue')
        self.assertEqual(new, self.test_file_1)
        self.assertTrue(os.path.isfile(self.test_file_1))
        found_entries = list(cuescanner.list_file_entries(self.test_file_1))
        # original file has incorrect file type
        ogg_tracks = tracks('MUSIC/Track{:02d}.ogg', 'MP3', 2, 9)
        expected = [('GAME.GOG', 'BINARY')] + ogg_tracks
        self.assertEqual(expected, found_entries)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
