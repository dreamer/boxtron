#!/usr/bin/env python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import os
import unittest

# Unit Tests are started with overriden XDG_CONFIG_HOME
from settings import SETTINGS as settings, DEFAULT_DOSBOX_BINARY


class TestSettings(unittest.TestCase):

    def setUp(self):
        self.original = settings.get_dosbox_bin()

    def tearDown(self):
        settings.set_dosbox_bin(' '.join(self.original))

    def test_dosbox_bin_file(self):
        expected = os.path.expanduser('~/bin/my-awesome-dosbox')
        self.assertEqual(settings.get_dosbox_bin(), [expected])

    def test_dosbox_bin_set_get(self):
        settings.set_dosbox_bin('dosbox')
        self.assertEqual(settings.get_dosbox_bin(), ['dosbox'])

    def test_dosbox_bin_tilde(self):
        expected = os.path.expanduser('~/bin/dosbox')
        settings.set_dosbox_bin('~/bin/dosbox')
        self.assertEqual(settings.get_dosbox_bin(), [expected])

    def test_dosbox_bin_command_1(self):
        settings.set_dosbox_bin('snap run dosbox-x # hello')
        self.assertEqual(settings.get_dosbox_bin(),
                         ['snap', 'run', 'dosbox-x'])

    def test_dosbox_bin_broken_command(self):
        settings.set_dosbox_bin('~/bin/foo bar ~/opt/baz"')
        self.assertEqual(settings.get_dosbox_bin(), [DEFAULT_DOSBOX_BINARY])

    def test_dosbox_bin_command_2(self):
        settings.set_dosbox_bin('~/bin/foo bar ~/opt/baz')
        bin_foo = os.path.expanduser('~/bin/foo')
        opt_baz = os.path.expanduser('~/opt/baz')
        self.assertEqual(settings.get_dosbox_bin(),
                         [bin_foo, 'bar', opt_baz])

    def test_dosbox_bin_command_whitespace(self):
        settings.set_dosbox_bin('/bin/foo\\ foo bar "/opt/baz baz/baz"')
        self.assertEqual(settings.get_dosbox_bin(),
                         ['/bin/foo foo', 'bar', '/opt/baz baz/baz'])

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
