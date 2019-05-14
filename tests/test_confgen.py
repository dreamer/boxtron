#!/usr/bin/env python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import unittest
import os

import confgen


class TestConfGenerator(unittest.TestCase):

    def test_example(self):
        name = confgen.uniq_conf_name('1234', ['foo'])
        self.assertEqual(name, 'steam_dos_1234_a63add.conf')


class TestDosboxConfiguration(unittest.TestCase):

    def setUp(self):
        self.original_dir = os.getcwd()

    def tearDown(self):
        os.chdir(self.original_dir)

    # $ dosbox -c 'foo' -c 'bar'
    # Z:\>foo
    # Z:\>bar
    #
    def test_config_with_commands(self):
        files = confgen.FileTree('tests/files/no_conf')
        cfg = confgen.DosboxConfiguration(files, commands=['foo', 'bar'])
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['foo', 'bar'])

    # $ dosbox file.exe
    # Z:\>mount C .
    # Z:\>file.exe
    #
    def test_config_single_exe(self):
        os.chdir('tests/files/no_conf')
        files = confgen.FileTree('.')
        cfg = confgen.DosboxConfiguration(files, exe='file.exe')
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['mount C .', 'C:', 'file.exe'])

    # $ dosbox -conf c1.conf
    # <autoexec section from c1.conf>
    #
    def test_config_from_conf(self):
        os.chdir('tests/files/confs')
        files = confgen.FileTree('.')
        cfg = confgen.DosboxConfiguration(files, conf_files=['c1.conf'])
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['echo c1'])

    # $ dosbox -conf c1.conf -conf c2
    # <autoexec section from c1.conf>
    # <autoexec section from c2.conf>
    #
    def test_config_from_conf_2(self):
        os.chdir('tests/files/confs')
        files = confgen.FileTree('.')
        cfg = confgen.DosboxConfiguration(files, conf_files=['c1.conf',
                                                             'c2.conf'])
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['echo c1', 'echo c2'])

    # $ dosbox -conf C1.conf
    # <autoexec section from c1.conf>
    #
    def test_config_from_conf_case_insensitive(self):
        os.chdir('tests/files/confs')
        files = confgen.FileTree('.')
        cfg = confgen.DosboxConfiguration(files, conf_files=['C1.conf'])
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['echo c1'])

    # $ dosbox -c cmd1 file.exe -c cmd2
    # Z:\>cmd1
    # Z:\>cmd2
    # Z:\>mount C .
    # C:\>file.exe

    # $ dosbox -c cmd1 -conf c1.conf -c cmd2
    # <autoexec section from c1.conf>
    # Z:\>cmd1
    # Z:\>cmd2

    # (when dosbox.conf with "cmd1" exists)
    # $ dosbox -c cmd2
    # Z:\>cmd1
    # Z:\>cmd2

    # (when dosbox.conf with "cmd1" exists and c2.conf with "cmd2" exists)
    # $ dosbox -conf c2.conf
    # Z:\>cmd2

    # (when DoSbOx.CoNf with "cmd1" exists)
    # $ dosbox -c cmd2
    # Z:\>cmd1
    # Z:\>cmd2

    # (when DoSbOx.CoNf with "cmd1" exists and C2.conf with "cmd2" exists)
    # $ dosbox -conf c2.conf
    # Z:\>cmd2


if __name__ == '__main__':
    unittest.main()
