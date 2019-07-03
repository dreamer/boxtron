#!/usr/bin/python3

"""
Fake iscriptevaluator.exe
"""
import os
import re
import subprocess
import time

import tweaks
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
    assert args
    last_arg = args[-1]

    if '--get-current-step' in args:
        steam_app_id = last_arg
        print('1/2:', steam_app_id, end='')
        return 0

    steam_app_id = 0
    script_name_pattern = re.compile(r'.*script_(\d+)\.vdf')
    match = script_name_pattern.match(last_arg)
    if match:
        steam_app_id = match.group(1)

    if not tweaks.download_tweak_needed(steam_app_id):
        return 0

    # run the post-installation process here, protect it with a PidFile
    print_err('steam-dos: downloading files for:', steam_app_id)
    time.sleep(4)
    status = 0
    return status
