#!/usr/bin/env python3

"""
Additional functionality for MIDI support.
"""

import collections
import re


MidiPort = collections.namedtuple('MidiPort', 'addr name desc space flags')


# I would very much prefer to implement this function using ctypes and
# alsa-lib, but that lib does not expose memory allocation functions
# as symbols (they are all macros), making it somewhat difficult to use
# from Python.
#
def list_alsa_sequencer_ports():
    """List all sequencer ports visible through ALSA procfs."""
    with open('/proc/asound/seq/clients') as clients:
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
                yield MidiPort(f'{client}:{port}', name, desc, space, flags)


# example usage
for mp in list_alsa_sequencer_ports():
    print(mp.addr, mp.name, mp.flags[1])
