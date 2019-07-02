#!/usr/bin/python3

"""
Fake iscriptevaluator.exe
"""
import os
import subprocess

from toolbox import print_err

STEAM_APP_ID = os.environ.get('SteamAppId', '0')

PID_FILE = '/tmp/steam_dos_{0}'.format(STEAM_APP_ID)


def wait_for_previous_process():
    """Wait for other process to end."""
    pid = 0
    try:
        with open(PID_FILE, 'r') as pid_file:
            pid = int(pid_file.read())
    except FileNotFoundError:
        pass
    if pid and os.path.isfile('/proc/{0}/cmdline'.format(pid)):
        print_err('steam-dos: waiting for process', pid, 'to stop',
                  'and delete file', PID_FILE)
        subprocess.call(['inotifywait', '-e', 'delete', PID_FILE])


def iscriptevaluator(args):
    """Pretend to be iscriptevaluator.exe program."""
    # if '--get-current-step' in cmd_line:
    #       steam expects a line on unbuffered (?) stdout in specific format:
    #       "1/3: Component X"
    #       Will be shown in Steam user interface as:
    #       "(2/3) Installing Component X…"
    #       Just return after writing to stdout
    #       Proton uses: sys.stdout.buffer.write

    assert args is not None
    # run the post-installation process here, protect it with a PidFile
    status = 0
    return status
