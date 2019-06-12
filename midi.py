#!/usr/bin/env python3

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

from toolbox import print_err

ALSA_SEQ_CLIENTS = '/proc/asound/seq/clients'

MidiPort = collections.namedtuple('MidiPort', 'addr name desc space flags')


# I would very much prefer to implement this function using ctypes and
# alsa-lib, but that lib does not expose memory allocation functions
# as symbols (they are all macros), making it somewhat difficult to use
# from Python.
#
def list_alsa_sequencer_ports(alsa_seq_clients=ALSA_SEQ_CLIENTS):
    """List all sequencer ports visible through ALSA procfs."""
    with open(alsa_seq_clients) as clients:
        client_pattern = re.compile(r'^Client +(\d+) : "(.*)" \[(.*)\]')
        port_pattern = re.compile(r'^  Port +(\d+) : "(.*)" \((.{4})\)')
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
                yield MidiPort(client + ':' + port, name, desc, space, flags)


def detect_software_synthesiser(name_expr, alsa_seq_clients=ALSA_SEQ_CLIENTS):
    """Return an input port, where client name matches expression."""
    client_name_pattern = re.compile(name_expr)
    for port in list_alsa_sequencer_ports(alsa_seq_clients):
        if port.flags[1] != 'W':
            continue
        match = client_name_pattern.match(port.name.lower())
        if match:
            return port
    return None


def start_timidity(sfont):
    """Start TiMidity++ process."""
    cmd = ['timidity', '-iA', '-x', 'soundfont {0}'.format(sfont)]
    proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.DEVNULL)
    print_err('steam-dos: Starting MIDI client (pid: {0})'.format(proc.pid))
    print_err('steam-dos: Using soundfont: {0}'.format(sfont))
    time.sleep(0.5)  # TODO properly wait until sequencer is online
    atexit.register(stop_software_midi_synth, proc.pid)


def start_fluidsynth(sfont):
    """Start FluidSynth process."""
    cmd = ['fluidsynth', '-a', 'pulseaudio', sfont]
    proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.DEVNULL)
    print_err('steam-dos: Starting MIDI client (pid: {0})'.format(proc.pid))
    print_err('steam-dos: Using soundfont: {}'.format(sfont))
    time.sleep(1.0)  # TODO properly wait until sequencer is online
    atexit.register(stop_software_midi_synth, proc.pid)


def stop_software_midi_synth(pid):
    """Stop software synthesiser process."""
    print_err('steam-dos: Stopping MIDI client {0}'.format(pid))
    os.kill(pid, signal.SIGTERM)  # TODO ProcessLookupError:
