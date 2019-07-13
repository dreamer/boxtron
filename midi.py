#!/usr/bin/python3

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

from settings import SETTINGS as settings
from toolbox import print_err, which

KNOWN_HARDWARE = r'casio|um-one'

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
                    yield MidiPort('{}:{}'.format(client, port), name, desc,
                                   space, flags)
    except FileNotFoundError:
        pass  # we want simply empty generator


def detect_midi_synthesiser(seq_clients=ALSA_SEQ_CLIENTS):
    """Detect MIDI synthesiser according to user preferences."""
    # First pass: according to user preference:
    # Second pass: look for known hardware:
    # Third pass: look for software synthesiser:
    port = match_port_by_name(r'XXXXTODOXXXX', seq_clients) or \
           match_port_by_name(KNOWN_HARDWARE, seq_clients) or \
           match_port_by_name(r'timidity|fluid', seq_clients)
    return port


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
    print_err('steam-dos: Starting MIDI client (pid: {0})'.format(proc.pid))
    print_err('steam-dos: Using soundfont: {0}'.format(sfont))
    time.sleep(1.0)  # TODO properly wait until sequencer is online
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


def setup_midi_soft_synth():
    """Detect or run and configure software MIDI synthesiser."""
    if not settings.get_midi_on():
        return

    if detect_midi_synthesiser():
        # Synthesiser is already running (maybe as a service).
        # There's no reason to start our own.
        return

    tool = settings.get_midi_tool()
    sfont = settings.get_midi_soundfont()

    preference_list = []
    if tool == 'timidity':
        preference_list = ['timidity', 'fluidsynth']
    elif tool == 'fluidsynth':
        preference_list = ['fluidsynth', 'timidity']

    for tool in preference_list:
        if not which(tool):
            continue
        if tool == 'timidity':
            start_timidity(sfont)
            return
        if tool == 'fluidsynth':
            start_fluidsynth(sfont)
            return
    print_err('steam-dos: warn: no software MIDI synthesiser available')
