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


## Features

* Lower input lag (compared to DOSBox inside Proton)
* Steam features working as expected (e.g. Steam Cloud, Controller settings or recording of time played)
* Better fullscreen support, especially on multi-monitor setups\*
* Steam Overlay working out of the box\*
* More [configuration options](https://github.com/dreamer/steam-dos/wiki/Configuration) and better defaults\*
* Auto-start of software MIDI synthesiser
* Auto-setup of MIDI for supported titles (click Play and enjoy pre-configured MIDI music)

<sub>\* - compared to vanilla DOSBox</sub>


## Prerequisites

You will need Python (>= 3.5), DOSBox (>= 0.74) and inotify-tools.
Optionally for MIDI support: TiMidity++ or FluidSynth and a soundfont.

#### Fedora

    $ sudo dnf install dosbox inotify-tools timidity++ fluid-soundfont-gm

#### OpenSUSE

    $ sudo zypper install dosbox inotify-tools timidity fluid-soundfont

#### Debian, Ubuntu et consortes

    $ sudo apt install dosbox inotify-tools timidity fluid-soundfont-gm

#### Arch, Manjaro

    $ sudo pacman -S dosbox inotify-tools timidity++ soundfont-fluid


## Installation (using tarball)

1. Close Steam.
2. Download and unpack tarball:

       $ cd ~/.local/share/Steam/compatibilitytools.d/ || cd ~/.steam/root/compatibilitytools.d/
       $ curl -L https://github.com/dreamer/steam-dos/releases/download/v0.4.0/steam-dos.tar.xz | tar xJf -

3. Start Steam.
4. In game properties window select "Force the use of a specific Steam Play
   compatibility tool" and select "DOSBox (native)".


## Installation (from source)

1. Close Steam.
2. Clone the repository and install the script to user directory:

       $ git clone https://github.com/dreamer/steam-dos.git
       $ cd steam-dos
       $ make user-install

3. Start Steam.
4. In game properties window select "Force the use of a specific Steam Play
   compatibility tool" and select "DOSBox (native)".


## Configuration

Read [Configuration](https://github.com/dreamer/steam-dos/wiki/Configuration) article on project Wiki.


## GOG Games

To easily install a DOS game from GOG to your Steam library, use included script:

    $ ./install-gog-game ~/Downloads/setup_warcraft_orcs__humans_1.2_\(28330\).exe

It will unpack the game to `~/.local/share/games`, prepare a setup that works around all
known Steam bugs and generate `.desktop` file to be added to your Steam library. After
that you can play the game using steam-dos or Proton.

Installation script depends only on Python standard library, you can put it in your
PATH or wherever you like.


## MIDI auto-setup

steam-dos preconfigures selected titles to turn MIDI music on/off, depending on user
preferences. Supported games are:

* [STAR WARS™ - Dark Forces](https://store.steampowered.com/app/32400/)
* [STAR WARS™ - X-Wing: Classic Edition](https://store.steampowered.com/app/354430/)
* [STAR WARS™ - X-Wing: Collector's CD-ROM Edition](https://store.steampowered.com/app/354430/)
* [X-COM: UFO Defense](https://store.steampowered.com/app/7760/)
* [X-COM: Terror From the Deep](https://store.steampowered.com/app/7650/)
* [Jagged Alliance Gold](https://store.steampowered.com/app/283270/)
* [Jagged Alliance Deadly Games](https://store.steampowered.com/app/283270/)
* [System Shock: Classic](https://steamdb.info/app/410700/)
* [The Ultimate DOOM](https://store.steampowered.com/app/2280/Ultimate_Doom/)
* [Final DOOM](https://store.steampowered.com/app/2290/Final_DOOM/)
* [DOOM II](https://store.steampowered.com/app/2300/DOOM_II/)
* [Master Levels for DOOM II](https://store.steampowered.com/app/9160/Master_Levels_for_Doom_II/)
* [Heretic: Shadow of the Serpent Riders](https://store.steampowered.com/app/2390/Heretic_Shadow_of_the_Serpent_Riders/)
* [Hexen: Beyond Heretic](https://store.steampowered.com/app/2360/HeXen_Beyond_Heretic/)


Just click "Play" and enjoy glorious MIDI music, there's no need to hunt those
pesky `SETSOUND.EXE` programs.

#### Other games

Sythesiser running does not automagically turn on MIDI music in every game,
sometimes you need to enable it manually (usually there's a file called `SETUP.EXE`,
`IMUSE.EXE` or similar somewhere in the game directory). Use following settings:

Music/device: **Roland MPU401/General MIDI**, Music Port: **330**

If you'll find a game, that supports MIDI and you need to enable it manually,
create a bug report, please!


## Sierra Launcher

Some game collections on Steam use "Sierra Classics Launcher" graphical frontend.
There's no support for graphical version of this launcher - the first game in a collection
will be started by default. You can select different game to run with `SDOS_SIERRA_GAME`
environment variable.

For example, to start King's Quest 6 from
[King's Quest Collection](https://store.steampowered.com/app/10100/):

    SDOS_SIERRA_GAME=6 %command%

Check `SierraLauncher.ini` file in game's installation dir to learn which number
corresponds to which game.


## Development

Read all about it in the [contributing guide](https://github.com/dreamer/steam-dos/blob/master/CONTRIBUTING.md) :)


## Known issues

As of June/July 2019 you are likely to encounter one of these bugs:

* Steam Overlay causes [visual glitch](https://github.com/dreamer/steam-dos/issues/8). DOSBox issue, fixed in 0.74-3.
* Mouse [cursor issues](https://github.com/dreamer/steam-dos/issues/7) in Gnome 3.30. Gnome issue, fixed in 3.32.
* Some games experience random KeyUp events. [DOSBox issue](https://www.vogons.org/viewtopic.php?f=31&t=66491).
* Alt+Tab does not work in fullscreen. DOSBox does not support borderless window mode (yet) - use **Alt+Enter** to leave fullscreen and interact with your desktop.
