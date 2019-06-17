#!/usr/bin/env python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import unittest

import preconfig

TAR1 = 'tests/files/resource/test.tar'


class TestPreconfig(unittest.TestCase):

    def test_file_filter(self):
        with preconfig.open_resource(TAR1) as resource_file:
            files = resource_file.filter_pfx('preconfig/')
            self.assertEqual(len(list(files)), 5)

    def test_file_content_1(self):
        with preconfig.open_resource(TAR1) as resource_file:
            self.assertTrue(resource_file.includes('32400'))

    def test_file_content_2(self):
        with preconfig.open_resource(TAR1) as resource_file:
            self.assertFalse(resource_file.includes('3240'))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
