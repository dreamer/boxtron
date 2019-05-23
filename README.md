# steam-dos

Compatibility tool to run DOS games on Steam through native Linux DOSBox version.

![steam-dos](https://user-images.githubusercontent.com/3967/57303584-f448b600-70dd-11e9-91f9-e7f45a8157f5.png)

Official mirrors:
[GitHub](https://github.com/dreamer/steam-dos),
[GitLab](https://gitlab.com/dreamer-tan/steam-dos).

## Prerequisites

You will need Python (>= 3.6), DOSBox (>= 0.74) and inotify-tools.
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

Steam-dos will start DOSBox in native desktop resolution and with OpenGL backend.
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

Makefile default target (`lint`) runs linters on project files, use it.
Run `make install` to easily put files in Steam's `compatibilitytools.d`
directory.

Steam will detect new tool being installed after you restart the client.
As long as you don't touch .vdf files, there's no need to keep restarting
it, though.

To run unit tests:

    make test

For coverage report, install [Coverage.py](https://coverage.readthedocs.io/)
(Fedora package `python3-coverage`).

    make coverage
