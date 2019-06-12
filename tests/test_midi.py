#!/usr/bin/env python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import unittest

import midi


class TestAlsaMidiClients(unittest.TestCase):

    def test_list_default(self):
        fake_seq_list = 'tests/files/alsa/default'
        found_ports = list(midi.list_alsa_sequencer_ports(fake_seq_list))
        self.assertEqual(len(found_ports), 4)

    def test_find_no_client(self):
        fake_seq_list = 'tests/files/alsa/default'
        port = midi.detect_software_synthesiser(r'foobar',
                                                alsa_seq_clients=fake_seq_list)
        self.assertEqual(port, None)

    def test_find_a_client(self):
        fake_seq_list = 'tests/files/alsa/fluid'
        port = midi.detect_software_synthesiser(r'fluid',
                                                alsa_seq_clients=fake_seq_list)
        self.assertEqual(port.addr, '128:0')
        self.assertEqual(port.space, 'User')
        self.assertEqual(port.flags, '-We-')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
