#!/usr/bin/python3

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
        port = midi.match_port_by_name(r'foobar', seq_clients=fake_seq_list)
        self.assertEqual(port, None)

    def test_find_a_client(self):
        fake_seq_list = 'tests/files/alsa/fluid'
        port = midi.match_port_by_name(r'fluid', seq_clients=fake_seq_list)
        self.assertEqual(port.addr, '128:0')
        self.assertEqual(port.space, 'User')
        self.assertEqual(port.flags, '-We-')

    def test_find_hw_um_one(self):
        fake_seq_list = 'tests/files/alsa/um-one'
        port = midi.detect_midi_synthesiser(seq_clients=fake_seq_list)
        self.assertEqual(port.addr, '24:0')

    def test_find_hw_casio(self):
        fake_seq_list = 'tests/files/alsa/casio'
        port = midi.detect_midi_synthesiser(seq_clients=fake_seq_list)
        self.assertEqual(port.addr, '16:0')

    def test_missing_sequencer_file(self):
        fake_seq_list = 'tests/files/alsa/missing_file'
        found_ports = list(midi.list_alsa_sequencer_ports(fake_seq_list))
        self.assertEqual(found_ports, [])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
