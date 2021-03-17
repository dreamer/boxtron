# Boxtron

[![Build Status](https://travis-ci.com/dreamer/boxtron.svg?branch=master)](https://travis-ci.com/dreamer/boxtron)
[![Luxtorpeda project Discord](https://img.shields.io/discord/514567252864008206.svg?label=discord)](https://discord.gg/8mFhUPX)

Steam Play compatibility tool to run DOS games using native Linux DOSBox

This is a sister project of
[Luxtorpeda](https://github.com/dreamer/luxtorpeda),
[Roberta](https://github.com/dreamer/roberta), and
[DOSBox Staging](https://dosbox-staging.github.io/).

![boxtron](https://user-images.githubusercontent.com/3967/111551660-fde2e080-8780-11eb-961a-f2fae8286cfa.png)

Official mirrors:
[GitHub](https://github.com/dreamer/boxtron),
[GitLab](https://gitlab.com/luxtorpeda/boxtron).

Game compatibility reports:
[Steam](https://github.com/dreamer/boxtron/wiki/Compatibility-reports),
[GOG](https://github.com/dreamer/boxtron/wiki/Compatibility-reports-(GOG)).


## Features

* Lower input lag (compared to DOSBox inside Proton)
* Steam features working as expected (e.g. Steam Cloud, Controller settings or recording of time played)
* Better fullscreen support, especially on multi-monitor setups\*
* Steam Overlay working out of the box\*
* More [configuration options](https://github.com/dreamer/boxtron/wiki/Configuration) and better defaults\*
* Automatic detection of MIDI hardware, with software synthesiser used as fallback
* Automatic MIDI setup for supported titles (click Play and enjoy pre-configured MIDI music)

<sub>\* - compared to vanilla DOSBox</sub>


## Installation (from repositories)

##### Flathub

If you use [Steam flatpak](https://flathub.org/apps/details/com.valvesoftware.Steam),
you can add Boxtron using:

    $ flatpak install flathub Boxtron

##### Arch, Manjaro

You can use [AUR package](https://aur.archlinux.org/packages/boxtron/).


## Installation (manual)

You'll need to install dependencies manually and then proceed to installation steps:
- [tarball (single-user)](#installation-using-tarball-for-a-single-user)
- [source (system-wide)](#installation-from-source-system-wide)
- [source (for development)](#installation-from-source-for-development)


### Dependencies

You will need Python (>= 3.5), DOSBox Staging (>= 0.76), inotify-tools,
TiMidity++, and a soundfont.  Optionally, you can use FluidSynth as well.
If your distribution does not include [dosbox-staging][dosbox-staging-repos]
yet, you can use DOSBox 0.74-3 instead, but you might encounter severe issues.

##### Fedora

    $ sudo dnf install dosbox-staging inotify-tools timidity++ fluid-soundfont-gm

##### OpenSUSE

    $ sudo zypper install dosbox inotify-tools timidity fluid-soundfont

##### Debian, Ubuntu, Mint, Pop!\_OS

    $ sudo apt install dosbox inotify-tools timidity fluid-soundfont-gm

##### Arch, Manjaro

    $ sudo pacman -S dosbox inotify-tools timidity++ soundfont-fluid

##### NixOS

    $ nix-env -f '<nixpkgs>' -iA dosbox inotify-tools timidity soundfont-fluid

[dosbox-staging-repos]: https://dosbox-staging.github.io/downloads/linux/

### Installation (using tarball, for a single user)

1. Download and unpack tarball to `compatibilitytools.d` directory (create one if it does not exist):

       $ cd ~/.local/share/Steam/compatibilitytools.d/ || cd ~/.steam/root/compatibilitytools.d/
       $ curl -L https://github.com/dreamer/boxtron/releases/download/v0.5.4/boxtron.tar.xz | tar xJf -

2. Start/restart Steam.
3. In game properties window go to "Compatibility" section, select "Force
   the use of a specific Steam Play compatibility tool" and pick
   "Boxtron (native DOSBox)".


### Installation (from source, system-wide)

This installation method is explained in detail in [the packaging guide](PACKAGING.md).

1. Clone the repository and install the script system-wide:

       $ git clone https://github.com/dreamer/boxtron.git
       $ cd boxtron
       $ sudo make install

2. Start/restart Steam.
3. In game properties window select "Force the use of a specific Steam Play
   compatibility tool" and select "Boxtron (native DOSBox)".


### Installation (from source, for development)

This method is appropriate for testing and development.
See: [contributing guide](CONTRIBUTING.md).

1. Clone the repository and install the script to user directory:

       $ git clone https://github.com/dreamer/boxtron.git
       $ cd boxtron
       $ make dev-install

2. Start/restart Steam.
3. In game properties window select "Force the use of a specific Steam Play
   compatibility tool" and select "Boxtron (dev)".


## Configuration

Read [Configuration](https://github.com/dreamer/boxtron/wiki/Configuration) article on project Wiki.


## GOG Games

To easily install a DOS game from GOG to your Steam library, use included script:

    $ ./install-gog-game ~/Downloads/setup_warcraft_orcs__humans_1.2_\(28330\).exe

It will unpack the game to `~/.local/share/games`, prepare a setup that works around all
known Steam bugs and generate `.desktop` file to be added to your Steam library. After
that, you can play the game using Boxtron or Proton.

Installation script depends only on the Python standard library; you can put it in your
PATH or wherever you like.


## MIDI auto-setup

Boxtron preconfigures selected titles to turn MIDI music on/off, depending on user
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
* [Master Levels for DOOM II](https://store.steampowered.com/app/9160/)
* [Heretic: Shadow of the Serpent Riders](https://store.steampowered.com/app/2390/)
* [Hexen: Beyond Heretic](https://store.steampowered.com/app/2360/)
* [Hexen: Deathkings of the Dark Citadel](https://store.steampowered.com/app/2370/)
* [Duke Nukem 3D (Classic)](https://steamdb.info/app/225140/info/)
* [King's Table - The Legend of Ragnarok](https://store.steampowered.com/app/719310/)


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

*For most Sierra games, you might be interested in using
[Roberta](https://github.com/dreamer/roberta/) instead of Boxtron.*

Some game collections on Steam use "Sierra Classics Launcher" graphical frontend.
There's no support for graphical version of this launcher - the first game in a collection
will be started by default. You can select different game to run with `BOXTRON_SIERRA_GAME`
environment variable.

For example, to start King's Quest 6 from
[King's Quest Collection](https://store.steampowered.com/app/10100/):

    BOXTRON_SIERRA_GAME=6 %command%

Check `SierraLauncher.ini` file in game's installation dir to learn which number
corresponds to which game.


## Known issues

As of March 2021 you might encounter one of the following bugs:

- Some games experience random KeyUp events in fullscreen.
  It's a [DOSBox bug](https://www.vogons.org/viewtopic.php?f=31&t=66491), use
  [DOSBox Staging] to avoid it.
- Alt+Tab does not work in fullscreen. It's a DOSBox bug, use
  [DOSBox Staging] to avoid it.
- Modern game controllers might not work at all. It's a DOSBox bug, use
  [DOSBox Staging] to avoid it.
- Steam Overlay causes [visual glitch][steam-overlay-glitch].
  This was a DOSBox bug - use DOSBox 0.74-3 or
  [DOSBox Staging] to avoid it.

[DOSBox Staging]: https://dosbox-staging.github.io/
[steam-overlay-glitch]: https://github.com/dreamer/boxtron/issues/8
