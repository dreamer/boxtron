# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2019-2021  Patryk Obara <patryk.obara@gmail.com>

"""
Additional functionality for MIDI support.
"""

import atexit
import collections
import os
import re
import signal
import subprocess
import time

import toolbox

from log import log, log_warn, log_err
from settings import SETTINGS as settings

# casio:   tested with Casio CTK-4200
# um-one:  tested with Roland's UM-ONE USB MIDI interface
# ensoniq: tested with Ensoniq AudioPCI
#
KNOWN_HARDWARE = r'casio|um-one|ensoniq|mpu-401 uart'

ALSA_SEQ_CLIENTS = '/proc/asound/seq/clients'

MidiPort = collections.namedtuple('MidiPort', 'addr name desc space flags')


# I would very much prefer to implement this function using ctypes and
# alsa-lib, but that lib does not expose memory allocation functions
# as symbols (they are all macros), making it somewhat difficult to use
# from Python.
#
def list_alsa_sequencer_ports(alsa_seq_clients=ALSA_SEQ_CLIENTS):
    """List all sequencer ports visible through ALSA procfs."""
    try:
        with open(alsa_seq_clients) as clients:
            client_pattern = re.compile(r'^ *Client +(\d+) *: "(.*)" \[(.*)\]')
            port_pattern = re.compile(r'^ *Port +(\d+) *: "(.*)" \((.{4})\)')
            client, name, space, port, desc, flags = '', '', '', '', '', ''
            for line in clients.readlines():
                match = client_pattern.match(line)
                if match:
                    client = match.group(1)
                    name = match.group(2)
                    space = match.group(3)
                    continue
                match = port_pattern.match(line)
                if match:
                    port = match.group(1)
                    desc = match.group(2)
                    flags = match.group(3)
                    yield MidiPort('{}:{}'.format(client, port), name, desc,
                                   space, flags)
    except FileNotFoundError:
        pass  # we want simply empty generator


def active_midi_through(alsa_seq_clients=ALSA_SEQ_CLIENTS):
    """Return 'Midi Through' port (14:0) if it's connected to something.

    If this port is connected to anything, whatever the purpose is, the user
    decided to pass through MIDI signal to some device - hardware or software.

    One possible use-case is to pass MIDI signal to software synthesiser
    running under Wine, e.g. Roland Sound Canvas VA.
    """
    try:
        with open(alsa_seq_clients) as clients:
            connected_from_pattern = re.compile(r'^\s*Connected From:\s+14:0')
            for line in clients.readlines():
                match = connected_from_pattern.match(line)
                if match:
                    port = MidiPort('14:0', 'Midi Through',
                                    'Midi Through Port-0', 'Kernel', '?W??')
                    return port
    except FileNotFoundError:
        pass
    return None


def find_midi_port(seq_clients=ALSA_SEQ_CLIENTS):
    """Find open MIDI port to connect to."""
    user_pref = settings.get_midi_sequencer()
    return match_port_by_name(user_pref, seq_clients) if user_pref else None \
        or match_port_by_name(KNOWN_HARDWARE, seq_clients) \
        or match_port_by_name(r'timidity|fluid', seq_clients) \
        or active_midi_through(seq_clients)


def match_port_by_name(name_expr=None, seq_clients=ALSA_SEQ_CLIENTS):
    """Return an input port, where client name matches expression."""
    client_name_pattern = re.compile(name_expr, re.IGNORECASE)
    for port in list_alsa_sequencer_ports(seq_clients):
        if port.flags[1] != 'W':
            continue
        match = client_name_pattern.match(port.name)
        if match:
            return port
    return None


def start_timidity(sfont):
    """Start TiMidity++ process."""
    cmd = ['timidity', '-iA', '-x', 'soundfont {0}'.format(sfont)]
    proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.DEVNULL)
    log('Starting MIDI client (pid: {0})'.format(proc.pid))
    log('Using soundfont: {0}'.format(sfont))
    time.sleep(1.0)  # TODO properly wait until sequencer is online
    atexit.register(stop_software_midi_synth, proc.pid)


def start_fluidsynth(sfont):
    """Start FluidSynth process."""
    cmd = ['fluidsynth', '-a', 'pulseaudio', sfont]
    proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.DEVNULL)
    log('Starting MIDI client (pid: {0})'.format(proc.pid))
    log('Using soundfont: {}'.format(sfont))
    time.sleep(1.0)  # TODO properly wait until sequencer is online
    atexit.register(stop_software_midi_synth, proc.pid)


def stop_software_midi_synth(pid):
    """Stop software synthesiser process."""
    log('Stopping MIDI client {0}'.format(pid))
    os.kill(pid, signal.SIGTERM)  # TODO ProcessLookupError:


def detect_external_synth():
    """Detect a synthesiser running in the background."""
    user_pref = settings.get_midi_sequencer()
    if user_pref:
        if match_port_by_name(user_pref):
            # We found user's preferred port.
            return True
        log('synthesiser matching', user_pref, 'not found')
    else:
        if find_midi_port():
            # Synthesiser is already running (maybe as a service).
            return True
        log('no synthesiser running in the background')
    return False


def start_midi_synth():
    """Start software MIDI synthesiser according to user preferences."""
    if not settings.get_midi_on():
        return

    # either user had preference but the preferred port was not found
    # or user had no preference and there was no appropriate port to use
    # so simply start one of software synthesisers as a fallback:

    tool = settings.get_midi_tool()
    sfont = settings.get_midi_soundfont()

    if not sfont:
        log_err("Can't start a software synthesiser without a soundfont")
        return

    preference_list = []
    if tool == 'timidity':
        preference_list = ['timidity', 'fluidsynth']
    elif tool == 'fluidsynth':
        preference_list = ['fluidsynth', 'timidity']

    log('Trying to start {} or {}'.format(*preference_list))

    for tool in preference_list:
        if not toolbox.which(tool):
            continue
        if tool == 'timidity':
            start_timidity(sfont)
            return
        if tool == 'fluidsynth':
            start_fluidsynth(sfont)
            return
    log_warn('no software MIDI synthesiser available')
