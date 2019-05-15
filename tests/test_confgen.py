#!/usr/bin/env python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import unittest
import os

import confgen


class TestConfGenerator(unittest.TestCase):

    def test_uniq_name(self):
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

    # $ dosbox -c cmd1 FILE.EXE -c cmd2  # when file.exe is present
    # Z:\>cmd1
    # Z:\>cmd2
    # Z:\>mount C .
    # Z:\>C:
    # C:\>file.exe
    #
    def test_config_cmds_and_exe(self):
        os.chdir('tests/files/no_conf')
        files = confgen.FileTree('.')
        cfg = confgen.DosboxConfiguration(files,
                                          exe='FILE.EXE',
                                          commands=['cmd1', 'cmd2'])
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['cmd1',
                                           'cmd2',
                                           'mount C .',
                                           'C:',
                                           'file.exe'])

    # $ dosbox -c cmd1 -conf c1.conf -c cmd2
    # <autoexec section from c1.conf>
    # Z:\>cmd1
    # Z:\>cmd2
    #
    def test_config_cmds_and_conf(self):
        os.chdir('tests/files/confs')
        files = confgen.FileTree('.')
        cfg = confgen.DosboxConfiguration(files,
                                          conf_files=['c1.conf'],
                                          commands=['cmd1', 'cmd2'])
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['echo c1',
                                           'cmd1',
                                           'cmd2'])

    # When dosbox.conf with "echo dosbox" exists:
    #
    # $ dosbox -c cmd
    # Z:\>echo dosbox
    # Z:\>cmd
    #
    def test_config_default_1(self):
        os.chdir('tests/files/default')
        files = confgen.FileTree('.')
        cfg = confgen.DosboxConfiguration(files, commands=['cmd'])
        self.assertEqual(cfg['autoexec'], ['echo dosbox', 'cmd'])

    # When dosbox.conf with "echo dosbox" exists and c.conf with "cmd" exists:
    #
    # $ dosbox -conf c.conf
    # Z:\>cmd
    def test_config_default_2(self):
        os.chdir('tests/files/default')
        files = confgen.FileTree('.')
        cfg = confgen.DosboxConfiguration(files, conf_files=['c.conf'])
        self.assertEqual(cfg['autoexec'], ['cmd'])

    # When DoSbOx.CoNf with "echo dOsBoX" exists:
    # $ dosbox -c foo
    # Z:\>echo dOsBoX
    # Z:\>foo
    def test_config_default_3(self):
        os.chdir('tests/files/case')
        files = confgen.FileTree('.')
        cfg = confgen.DosboxConfiguration(files, commands=['foo'])
        self.assertEqual(cfg['autoexec'], ['echo dOsBoX', 'foo'])

    # Multiple .conf files with missing or empty autoexec
    #
    def test_config_no_autoexec(self):
        os.chdir('tests/files/confs')
        files = confgen.FileTree('.')
        cfg = confgen.DosboxConfiguration(files,
                                          conf_files=['no_autoexec.conf',
                                                      'empty_autoexec.conf'])
        self.assertEqual(cfg['autoexec'], [])


if __name__ == '__main__':
    unittest.main()
