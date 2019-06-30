#!/usr/bin/python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import os
import unittest

from winpathlib import to_posix_path


class TestPathConversion(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(to_posix_path(''), '')

    def test_path_none(self):
        with self.assertRaises(TypeError):
            to_posix_path(None)

    def test_dot(self):
        self.assertEqual(to_posix_path('.'), '.')

    def test_dots(self):
        self.assertEqual(to_posix_path('..'), '..')

    def test_dots_2(self):
        self.assertEqual(to_posix_path('.\\..'), '..')
        self.assertEqual(to_posix_path('..\\..'), '../..')

    def test_simple_paths(self):
        self.assertEqual(to_posix_path('tests'), 'tests')
        self.assertEqual(to_posix_path('TeStS'), 'tests')

    def test_longer_paths_1(self):
        win_path = 'TESTS\\FILES\\CONFS\\ABC\\DEF\\FILE'
        lin_path = 'tests/files/confs/abc/DEF/file'
        self.assertEqual(to_posix_path(win_path), lin_path)

    def test_longer_paths_2(self):
        win_path = 'tests\\files\\case\\dosbox.conf'
        lin_path = 'tests/files/case/DoSbOx.CoNf'
        self.assertEqual(to_posix_path(win_path), lin_path)

    def test_longer_paths_3(self):
        win_path = 'tests\\files\\..\\files\\.\\.\\case\\dosbox.conf'
        lin_path = 'tests/files/../files/case/DoSbOx.CoNf'
        self.assertEqual(to_posix_path(win_path), lin_path)

    def test_missing_path(self):
        win_path = 'tests\\files\\case\\dosbox.confz'
        self.assertEqual(to_posix_path(win_path), None)

    def test_missing_path_2(self):
        win_path = 'tests_XXX\\files\\case\\dosbox.confz'
        self.assertEqual(to_posix_path(win_path), None)

    def test_really_long_path(self):
        path = 'tests/files/somewhat_long_path/'
        file = 'With Much Much Longer Path Inside ' + \
               'AbcDefGhiJklMnoPqrStuVwxYz_0123456789.tXt'
        win_path = (path + file).replace('\\', '/').upper()
        self.assertEqual(to_posix_path(win_path), path + file)

    def test_tricky_path(self):
        win_path = 'tests\\files\\CASE\\a\\B\\c'
        lin_path = 'tests/files/case/A/b/C'
        self.assertTrue(os.path.exists(lin_path))
        self.assertTrue(os.path.exists('tests/files/case/a/B'))
        self.assertFalse(os.path.exists('tests/files/case/a/B/C'))
        self.assertEqual(to_posix_path(win_path), lin_path)

    def test_ambiguous_path_lenient(self):
        win_path = 'tests\\files\\CASE\\a\\B\\file'
        lin_path_1 = 'tests/files/case/A/b/file'
        lin_path_2 = 'tests/files/case/a/B/file'
        self.assertTrue(os.path.exists(lin_path_1))
        self.assertTrue(os.path.exists(lin_path_2))
        self.assertIn(to_posix_path(win_path, strict=False),
                      (lin_path_1, lin_path_2))

    def test_ambiguous_path_strict(self):
        win_path = 'tests\\files\\CASE\\a\\B\\file'
        lin_path_1 = 'tests/files/case/A/b/file'
        lin_path_2 = 'tests/files/case/a/B/file'
        self.assertTrue(os.path.exists(lin_path_1))
        self.assertTrue(os.path.exists(lin_path_2))
        with self.assertRaises(FileNotFoundError):
            to_posix_path(win_path, strict=True)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
