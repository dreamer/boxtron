This directory contains configuration files to automatically enable/disable
MIDI support in various DOS games.

Files with extension .rpatch define regular expressions (using Python syntax)
for modification of textual configuration files, if possible.

Directories midi_on/off contain configuration files in various binary formats,
for different games.

midi_off:
  Digital sound:
    Sound Blaster 16, base 220, irq 7, dma 1, hdma 5, as many channels as possible
  MIDI:
    either off or set to the same values as digital sound

midi_on:
  Digital sound:
    Sound Blaster 16, base 220, irq 7, dma 1, hdma 5, as many channels as possible
  MIDI:
    Roland MPU401/General MIDI, port 330

If the game supports other options - then all defaults are preserved.

Files in this directory are NOT copyrighted.
