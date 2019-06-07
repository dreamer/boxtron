# steam-dos

[![Build Status](https://travis-ci.com/dreamer/steam-dos.svg?branch=master)](https://travis-ci.com/dreamer/steam-dos)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/dreamer)


Compatibility tool to run DOS games on Steam through native Linux DOSBox version.

![steam-dos](https://user-images.githubusercontent.com/3967/57303584-f448b600-70dd-11e9-91f9-e7f45a8157f5.png)

Official mirrors:
[GitHub](https://github.com/dreamer/steam-dos),
[GitLab](https://gitlab.com/dreamer-tan/steam-dos).

## Prerequisites

You will need Python (>= 3.5), DOSBox (>= 0.74) and inotify-tools.
Optionally for MIDI support: TiMidity++ or FluidSynth and a soundfont.

#### Fedora

    $ sudo dnf install dosbox inotify-tools timidity++ fluid-soundfont-gm

#### Debian, Ubuntu et consortes

    $ sudo apt install dosbox inotify-tools timidity fluid-soundfont-gm

#### Arch, Manjaro

    $ sudo pacman -S dosbox inotify-tools timidity++ soundfont-fluid


## Installation (using tarball)

1. Close Steam.
2. Download and unpack tarball:

       $ cd ~/.local/share/Steam/compatibilitytools.d/ || cd ~/.steam/root/compatibilitytools.d/
       $ curl -L https://github.com/dreamer/steam-dos/releases/download/v0.2.1/steam-dos-0.2.tar.xz | tar xJf -

3. Start Steam.
4. In game properties window select "Force the use of a specific Steam Play
   compatibility tool" and select "DOSBox (native)".


## Features

steam-dos will start DOSBox in native desktop resolution and with OpenGL backend.
These options are needed for Steam Overlay support and to prevent changing resolution
on modern displays.  It also seems to be performing much better than DOSBox defaults.

If you want to modify DOSBox settings for a game, edit `steam_dos_<appid>_<id>.conf`
file in game's installation dir. Remove it to force steam-dos to create a new one.

Settings for steam-dos can be found in `~/.config/steam-dos.conf` (or wherever
`XDG_CONFIG_HOME` points to).

## MIDI support

TiMidity++ (or FluidSynth) are started and closed automatically, unless they are already
working in the background.  You can turn it off by changing an option in settings file
(`~/.config/steam-dos.conf`) or using `SDOS_NO_MIDI=1` environment variable.
Soundfont `FluidR3_GM.sf2` is used by default - you can change it by editing settings file.

NOTE: Sythesiser running does not automagically turn on MIDI music in your game,
you need to enable it manually (usually there's a file called `SETUP.EXE`,
`IMUSE.EXE` or similar somewhere in the game directory). Use following settings:

Music/device: "General MIDI", Music Port: **330**

## Caution!

* There's no official Steam Cloud support, but it seems to be working - use at your
  own risk. You can disable this feature for now by unselecting:
 *Properties → Updates → Enable Steam Cloud Synchronization…*

* Do not select "DOSBox (native)" as default compatibility tool in Steam Play
  settings - it might prevent games from being installed.

## Development

Read all about it in the [contributing guide](https://github.com/dreamer/steam-dos/blob/master/CONTRIBUTING.md) :)
