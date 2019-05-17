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
    def test_autoexec_with_commands(self):
        os.chdir('tests/files/no_conf')
        cfg = confgen.DosboxConfiguration(commands=['foo', 'bar'])
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['foo', 'bar'])

    # $ dosbox file.exe
    # Z:\>mount C .
    # Z:\>file.exe
    #
    def test_autoexec_single_exe(self):
        os.chdir('tests/files/no_conf')
        cfg = confgen.DosboxConfiguration(exe='file.exe')
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['mount C .', 'C:', 'file.exe'])

    # $ dosbox -conf c1.conf
    # <autoexec section from c1.conf>
    #
    def test_autoexec_from_conf(self):
        os.chdir('tests/files/confs')
        cfg = confgen.DosboxConfiguration(conf_files=['c1.conf'])
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['echo c1'])

    # $ dosbox -conf c1.conf -conf c2
    # <autoexec section from c1.conf>
    # <autoexec section from c2.conf>
    #
    def test_autoexec_from_conf_2(self):
        os.chdir('tests/files/confs')
        cfg = confgen.DosboxConfiguration(conf_files=['c1.conf', 'c2.conf'])
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['echo c1', 'echo c2'])

    # $ dosbox -conf C1.conf
    # <autoexec section from c1.conf>
    #
    def test_autoexec_from_conf_3(self):
        os.chdir('tests/files/confs')
        cfg = confgen.DosboxConfiguration(conf_files=['C1.conf'])
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['echo c1'])

    # $ dosbox -c cmd1 FILE.EXE -c cmd2  # when file.exe is present
    # Z:\>cmd1
    # Z:\>cmd2
    # Z:\>mount C .
    # Z:\>C:
    # C:\>file.exe
    #
    def test_autoexec_cmds_and_exe(self):
        os.chdir('tests/files/no_conf')
        cfg = confgen.DosboxConfiguration(exe='FILE.EXE',
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
    def test_autoexec_cmds_and_conf(self):
        os.chdir('tests/files/confs')
        cfg = confgen.DosboxConfiguration(conf_files=['c1.conf'],
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
    def test_autoexec_default_1(self):
        os.chdir('tests/files/default')
        cfg = confgen.DosboxConfiguration(commands=['cmd'])
        self.assertEqual(cfg['autoexec'], ['echo dosbox', 'cmd'])

    # When dosbox.conf with "echo dosbox" exists and c.conf with "cmd" exists:
    #
    # $ dosbox -conf c.conf
    # Z:\>cmd
    def test_autoexec_default_2(self):
        os.chdir('tests/files/default')
        cfg = confgen.DosboxConfiguration(conf_files=['c.conf'])
        self.assertEqual(cfg['autoexec'], ['cmd'])

    # When DoSbOx.CoNf with "echo dOsBoX" exists:
    # $ dosbox -c foo
    # Z:\>echo dOsBoX
    # Z:\>foo
    def test_autoexec_default_3(self):
        os.chdir('tests/files/case')
        cfg = confgen.DosboxConfiguration(commands=['foo'])
        self.assertEqual(cfg['autoexec'], ['echo dOsBoX', 'foo'])

    # Multiple .conf files with missing or empty autoexec
    #
    def test_autoexec_no_autoexec(self):
        os.chdir('tests/files/confs')
        cfg = confgen.DosboxConfiguration(conf_files=['no_autoexec.conf',
                                                      'empty_autoexec.conf'])
        self.assertEqual(cfg['autoexec'], [])

    # Configuration files with sections other than autoexec:
    #
    def test_update_sections(self):
        os.chdir('tests/files/confs')
        cfg = confgen.DosboxConfiguration(conf_files=['sb1.conf', 'sb2.conf'])
        self.assertIn('sblaster', cfg.sections())
        self.assertIn('mixer', cfg.sections())
        self.assertEqual('44100', cfg['mixer']['rate'])  # from sb2.conf
        self.assertEqual('77', cfg['sblaster']['irq'])  # from sb2.conf
        self.assertEqual('42', cfg['sblaster']['dma'])  # from sb1.conf

    def test_fix_autoexec_1(self):
        os.chdir('tests/files/confs')
        old = ['mount c .', '@mount d .']
        new = ['mount C "."', 'mount D "."']
        self.assertEqual(list(confgen.to_linux_autoexec(old)), new)

    def test_fix_autoexec_2(self):
        os.chdir('tests/files/confs')
        old = ['mount c .. -type cdrom', 'c:', 'MOUNT d ".."', r'D:\ ']
        new = ['mount C ".." -type cdrom', 'C:', 'mount D ".."', 'D:']
        self.assertEqual(list(confgen.to_linux_autoexec(old)), new)

    def test_fix_autoexec_3(self):
        os.chdir('tests/files/confs')
        old = ['mount c dir', '@mount D "a b"', 'MOUNT E ABC\\DEF']
        new = ['mount C "Dir"', 'mount D "A B"', 'mount E "abc/DEF"']
        self.assertEqual(list(confgen.to_linux_autoexec(old)), new)

    def test_fix_autoexec_4(self):
        os.chdir('tests/files/confs')
        old = ['IMGMOUNT c dir/file', '@imgmount D "DIR/FILE"']
        new = ['imgmount C "Dir/file"', 'imgmount D "Dir/file"']
        self.assertEqual(list(confgen.to_linux_autoexec(old)), new)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
