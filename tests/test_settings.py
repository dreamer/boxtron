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

    def test_dosbox_setup(self):
        self.assertFalse(settings.finalized)
        settings.setup()
        self.assertTrue(settings.finalized)

    def test_set_value(self):
        settings.set_midi_on(False)
        self.assertFalse(settings.get_midi_on())
        settings.set_midi_on(True)
        self.assertTrue(settings.get_midi_on())


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
