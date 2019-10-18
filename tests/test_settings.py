#!/usr/bin/python3

# Copyright (C) 2019 Patryk Obara <patryk.obara@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import os
import unittest

# Unit Tests are started with overriden XDG_CONFIG_HOME
from settings import SETTINGS as settings, DEFAULT_DOSBOX_BINARY


class TestSettings(unittest.TestCase):

    def setUp(self):
        self.original = settings.get_dosbox_cmd()

    def tearDown(self):
        settings.set_dosbox_cmd(' '.join(self.original))
        os.environ.pop('BOXTRON_DOSBOX_CMD', None)

    def test_dosbox_cmd_file(self):
        expected = os.path.expanduser('~/bin/my-awesome-dosbox')
        self.assertEqual(settings.get_dosbox_cmd(), [expected])

    def test_dosbox_cmd_set_get(self):
        settings.set_dosbox_cmd('dosbox')
        self.assertEqual(settings.get_dosbox_cmd(), ['dosbox'])

    def test_dosbox_cmd_tilde(self):
        expected = os.path.expanduser('~/bin/dosbox')
        settings.set_dosbox_cmd('~/bin/dosbox')
        self.assertEqual(settings.get_dosbox_cmd(), [expected])

    def test_dosbox_cmd_command_1(self):
        settings.set_dosbox_cmd('snap run dosbox-x # hello')
        self.assertEqual(settings.get_dosbox_cmd(),
                         ['snap', 'run', 'dosbox-x'])

    def test_dosbox_cmd_broken_command(self):
        settings.set_dosbox_cmd('~/bin/foo bar ~/opt/baz"')
        self.assertEqual(settings.get_dosbox_cmd(), [DEFAULT_DOSBOX_BINARY])

    def test_dosbox_cmd_command_2(self):
        settings.set_dosbox_cmd('~/bin/foo bar ~/opt/baz')
        bin_foo = os.path.expanduser('~/bin/foo')
        opt_baz = os.path.expanduser('~/opt/baz')
        self.assertEqual(settings.get_dosbox_cmd(),
                         [bin_foo, 'bar', opt_baz])

    def test_dosbox_cmd_command_whitespace(self):
        settings.set_dosbox_cmd('/bin/foo\\ foo bar "/opt/baz baz/baz"')
        self.assertEqual(settings.get_dosbox_cmd(),
                         ['/bin/foo foo', 'bar', '/opt/baz baz/baz'])

    def test_dosbox_cmd_env_override(self):
        os.environ['BOXTRON_DOSBOX_CMD'] = 'test'
        self.assertEqual(settings.get_dosbox_cmd(), ['test'])

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
