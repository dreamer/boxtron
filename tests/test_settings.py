#!/usr/bin/env python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import os
import unittest

# Unit Tests are started with overriden XDG_CONFIG_HOME
from settings import SETTINGS as settings


class TestSettings(unittest.TestCase):

    def test_dosbox_bin(self):
        expected = os.path.expanduser('~/bin/my-awesome-dosbox')
        self.assertEqual(settings.get_dosbox_bin(), expected)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
