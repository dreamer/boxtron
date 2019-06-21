# steam-dos

[![Build Status](https://travis-ci.com/dreamer/steam-dos.svg?branch=master)](https://travis-ci.com/dreamer/steam-dos)
[![steam-dos discord](https://img.shields.io/discord/514567252864008206.svg?label=discord)](https://discord.gg/8mFhUPX)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/dreamer)

Compatibility tool to run DOS games on Steam through native Linux DOSBox.

![steam-dos](https://user-images.githubusercontent.com/3967/57303584-f448b600-70dd-11e9-91f9-e7f45a8157f5.png)

Official mirrors:
[GitHub](https://github.com/dreamer/steam-dos),
[GitLab](https://gitlab.com/dreamer-tan/steam-dos).

Game compatibility reports:
[Steam](https://github.com/dreamer/steam-dos/wiki/Compatibility-reports-(Steam)),
[GOG](https://github.com/dreamer/steam-dos/wiki/Compatibility-reports-(GOG)).

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
       $ curl -L https://github.com/dreamer/steam-dos/releases/download/v0.3.4/steam-dos.tar.xz | tar xJf -

3. Start Steam.
4. In game properties window select "Force the use of a specific Steam Play
   compatibility tool" and select "DOSBox (native)".


## Features

Settings for steam-dos can be found in `~/.config/steam-dos.conf` (or wherever
`XDG_CONFIG_HOME` points to).  New versions of steam-dos add new documentation
and options to that file - remove it to force steam-dos to create a fresh one
(including documentation for all new options).

If you want to modify DOSBox settings for a specific game, edit
`steam_dos_<appid>_<id>.conf` file in game's installation dir. Remove it to
force steam-dos to create a new one.

### Proper fullscreen support

steam-dos will start DOSBox in fullscreen on your primary display, without changing
resolution of your screens - just as any modern game does by default.

You can pick different screen by changing option `dosbox.fullscreenmode` in settings
file or using `SDOS_SCREEN=<num>` environment variable.

### MIDI support

TiMidity++ (or FluidSynth) are started and closed automatically, unless they are already
working in the background.  You can turn this feature off by changing an option in
settings file (`~/.config/steam-dos.conf`) or using `SDOS_NO_MIDI=1` environment variable.
Soundfont `FluidR3_GM.sf2` is used by default - you can change it by editing settings file.

NOTE: Sythesiser running does not automagically turn on MIDI music in your game,
you need to enable it manually (usually there's a file called `SETUP.EXE`,
`IMUSE.EXE` or similar somewhere in the game directory). Use following settings:

Music/device: **Roland MPU401/General MIDI**, Music Port: **330**

### Selecting different DOSBox builds

In `~/.config/steam-dos.conf`:

    [dosbox]
    cmd = ~/path_to_dosbox/src/dosbox

### GOG Games

To easily install a DOS game from GOG to your Steam library, use included script:

    $ ./install-gog-game ~/Downloads/setup_warcraft_orcs__humans_1.2_\(28330\).exe

It will unpack the game to `~/.local/share/games`, prepare a setup that works around all
known Steam bugs and generate `.desktop` file to be added to your Steam library. After
that you can play the game using steam-dos or Proton.

Installation script depends only on Python standard library, you can put it in your
PATH or wherever you like.

### Sierra Launcher

Some game collections on Steam use "Sierra Classics Launcher" graphical frontend.
There's no support for graphical version of this launcher - the first game in a collection
will be started by default. You can select different game to run with `SDOS_SIERRA_GAME`
environment variable.

For example, to start King's Quest 6 from
[King's Quest Collection](https://store.steampowered.com/app/10100/):

    SDOS_SIERRA_GAME=6 %command%

Check `SierraLauncher.ini` file in game's installation dir to learn which number
corresponds to which game.

## Caution!

* There's no official Steam Cloud support, but it seems to be working - use at your
  own risk. You can disable this feature for now by unselecting:
 *Properties → Updates → Enable Steam Cloud Synchronization…*

* Do not select "DOSBox (native)" as default compatibility tool in Steam Play
  settings - it might prevent games from being installed.

## Development

Read all about it in the [contributing guide](https://github.com/dreamer/steam-dos/blob/master/CONTRIBUTING.md) :)
