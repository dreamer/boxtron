#!/usr/bin/python3

# Copyright (C) 2019 Patryk Obara <patryk.obara@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import unittest

import xlib


class TestXlib(unittest.TestCase):

    def test_no_exception(self):
        # There's not much we can test here without conditionally
        # disabling tests on CI…
        screens = xlib.query_screens()
        self.assertEqual(screens.__class__, dict)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
