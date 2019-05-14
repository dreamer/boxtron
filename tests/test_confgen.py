#!/usr/bin/env python3

# pylint: disable=missing-docstring

import unittest

import confgen


class TestConfGenerator(unittest.TestCase):

    def test_example(self):
        name = confgen.uniq_conf_name('1234', ['foo'])
        self.assertEqual(name, 'steam_dos_1234_a63add.conf')


if __name__ == '__main__':
    unittest.main()
