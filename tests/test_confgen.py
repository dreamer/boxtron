#!/usr/bin/python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import os
import unittest

import confgen


class TestConfGenerator(unittest.TestCase):

    def test_uniq_name(self):
        name = confgen.uniq_conf_name('1234', ['foo'])
        self.assertEqual(name, 'steam_dos_1234_4eaf56.conf')


class TestDosboxArgParser(unittest.TestCase):

    # All Apogee titles have hanging '-c' as last argument.
    #
    def test_hanging_command(self):
        dargs = confgen.parse_dosbox_arguments(['-conf', r'..\\STARGUN.conf',
                                                '-noconsole', '-c'])
        self.assertEqual(dargs.c, [])

    # X-COM: Terror from the Deep has no special parameters at all:
    #
    def test_no_commands(self):
        dargs = confgen.parse_dosbox_arguments(['-conf', 'dosbox.conf'])
        self.assertEqual(dargs.c, [])
        self.assertEqual(dargs.conf, ['dosbox.conf'])


def raw_autoexec_section(path):
    out = False
    with open(path, 'r') as txt:
        for line in txt:
            if out:
                yield line.rstrip()
            if line.startswith('[autoexec]'):
                out = True


class TestDosboxConfiguration(unittest.TestCase):

    # pylint: disable=too-many-public-methods

    def setUp(self):
        self.tmp_user_file = 'user_file_test.conf'
        self.clean_after_test = ''
        self.original_dir = os.getcwd()

    def tearDown(self):
        if os.path.isfile(self.tmp_user_file):
            os.remove(self.tmp_user_file)
        if os.path.isfile(self.clean_after_test):
            os.remove(self.clean_after_test)
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

    # $ dosbox file.bat
    # Z:\>mount C .
    # Z:\>call file.bat
    #
    def test_autoexec_single_bat(self):
        os.chdir('tests/files/no_conf')
        cfg = confgen.DosboxConfiguration(exe='file.bat')
        self.assertIn('autoexec', cfg.sections())
        self.assertEqual(cfg['autoexec'], ['mount C .', 'C:', 'call file.bat'])

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

    def test_fix_autoexec_0(self):
        os.chdir('tests/files/confs')
        old = ['foo', 'bar baz']
        self.assertEqual(list(confgen.to_linux_autoexec(old)), old)

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

    # Warcraft: Orcs & Humans
    #
    # Using .conf files distributed through GOG after being added
    # as non-Steam game to Steam library:
    #
    def test_gog_warcraft(self):
        os.chdir('tests/files/gog/warcraft_orcs_and_humans/DOSBOX')
        cmd_line = ['-conf', '..\\dosbox_warcraft.conf',
                    '-conf', '..\\dosbox_warcraft_single.conf',
                    '-noconsole', '-c', 'exit']
        args = confgen.parse_dosbox_arguments(cmd_line)
        conf = confgen.DosboxConfiguration(conf_files=(args.conf or []),
                                           commands=args.c,
                                           exe=args.file,
                                           noautoexec=args.noautoexec,
                                           exit_after_exe=args.exit)
        # at the very least, autoexec should be filled
        self.assertEqual(conf.encoding, 'cp1250')

    # Arctic Adventure 1, 2, 3, 4
    #
    # Autoexec section implements simple game selector.
    #
    # Original file uses the same convention for mount command as we do,
    # so we can test if re-interpreted autoexec section is exactly the
    # same.
    #
    def test_arctic_adventure(self):
        os.chdir('tests/files/steam/arctic_adventure/Dosbox')
        cmd_line = ['-conf', r'..\Artic.conf', '-noconsole', '-c']
        args = confgen.parse_dosbox_arguments(cmd_line)
        conf = confgen.DosboxConfiguration(conf_files=(args.conf or []),
                                           commands=args.c,
                                           exe=args.file,
                                           noautoexec=args.noautoexec,
                                           exit_after_exe=args.exit)
        confgen.create_user_conf_file(self.tmp_user_file, conf, cmd_line)
        raw_autoexec = list(raw_autoexec_section('../ARTIC.conf'))
        old, old_enc = confgen.parse_dosbox_config('../ARTIC.conf')
        new, new_enc = confgen.parse_dosbox_config(self.tmp_user_file)
        old_autoexec = old.get_autoexec()
        new_autoexec = new.get_autoexec()
        self.assertEqual(old_enc, new_enc)
        self.assertEqual(raw_autoexec, old_autoexec)
        self.assertEqual(old_autoexec, new_autoexec)

    # Simplest test, just to make sure the file is being created.
    #
    def test_dummy_auto_config(self):
        os.chdir('tests/files/confs')
        cmd_line = ['-conf', 'empty_autoexec.conf']
        conf = confgen.create_dosbox_configuration(cmd_line, tweak_conf={})
        auto_conf = confgen.create_auto_conf_file(conf)
        self.clean_after_test = auto_conf
        self.assertTrue(os.path.isfile(auto_conf))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
