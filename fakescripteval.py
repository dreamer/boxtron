#!/usr/bin/python3

"""
Fake iscriptevaluator.exe
"""
import os
import re
import subprocess
# import time
import urllib.request
import shutil

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
        #print('1/2:', steam_app_id, end='')
        print('1/3: Hello, Faalagorn', end='')
        return 0

    steam_app_id = 0
    script_name_pattern = re.compile(r'.*script_(\d+)\.vdf')
    match = script_name_pattern.match(last_arg)
    if match:
        steam_app_id = match.group(1)

    if not tweaks.download_tweak_needed(steam_app_id):
        return 0

    # run the post-installation process here, protect it with a PidFile
    # time.sleep(4)

    download_links = tweaks.TWEAKS_DB[steam_app_id]['download']
    n = len(download_links)
    i = 0
    for name, desc in download_links.items():
        url = desc['url']
        cache_file = os.path.expanduser('~/.cache/' + name)
        if os.path.isfile(cache_file):
            continue
        print_err(f'steam-dos: downloading {i}/{n}: {url} -> {cache_file}')
        with urllib.request.urlopen(url) as resp, open(cache_file, 'wb') as out:
            shutil.copyfileobj(resp, out)
        i += 1

    status = 0
    return status
