#!/usr/bin/python3

# Copyright (C) 2019 Patryk Obara <patryk.obara@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import os
import unittest

import preconfig

TAR_TEST_DIR = 'tests/files/resource/'

TAR1 = TAR_TEST_DIR + 'test.tar'


class TestPreconfig(unittest.TestCase):

    def setUp(self):
        if os.path.isfile('file'):
            raise FileExistsError("remove 'file', please")  # pragma: no cover

    def tearDown(self):
        if os.path.isfile('file'):
            os.remove('file')

    def test_find_1(self):
        rfile = preconfig.find_resource_file()
        self.assertTrue(rfile.endswith('preconfig.tar'))
        # with preconfig.open_resource(rfile) as resource_file:
        #    resource_file.tar.list()

    def test_find_missing(self):
        sys_argv_0 = TAR_TEST_DIR + 'missing/exe'
        self.assertIsNone(preconfig.find_resource_file(sys_argv_0))

    def test_find_not_a_tar(self):
        sys_argv_0 = TAR_TEST_DIR + 'broken/exe'
        self.assertIsNone(preconfig.find_resource_file(sys_argv_0))

    def test_verify_preconfig(self):
        self.assertEqual(preconfig.CHECKSUM, preconfig.__checksum__())
        self.assertTrue(preconfig.verify())

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

    def test_extract_1(self):
        self.assertFalse(os.path.isfile('file'))
        with preconfig.open_resource(TAR1) as resource_file:
            resource_file.extract('32400', 'midi_on')
        self.assertTrue(os.path.isfile('file'))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
