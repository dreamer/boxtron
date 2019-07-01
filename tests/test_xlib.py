#!/usr/bin/python3

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
