# steam-dos

Compatibility tool to run DOS games on Steam through native Linux DOSBox version.

![steam-dos](https://user-images.githubusercontent.com/3967/57303584-f448b600-70dd-11e9-91f9-e7f45a8157f5.png)

## Prerequisites

You will need Python (>= 3.6), DOSBox (>= 0.74) and inotify-tools.

#### Fedora

    $ sudo dnf install dosbox inotify-tools

#### Debian, Ubuntu et consortes

    $ sudo apt install dosbox inotify-tools


## Installation (using tarball)

1. Close Steam.
2. Download and unpack tarball:

       $ cd ~/.local/share/Steam/compatibilitytools.d/ || cd ~/.steam/root/compatibilitytools.d/
       $ curl -L https://github.com/dreamer/steam-dos/releases/download/v0.1.1/steam-dos-0.1.tar.xz | tar xJf -

3. Start Steam.
4. In game properties window select "Force the use of a specific Steam Play
   compatibility tool" and select "DOSBox (native)".


## Features

Steam-dos will start DOSBox in native desktop resolution and with OpenGL backend.
These options are needed for Steam Overlay support and to prevent changing resolution
on modern displays.  It also seems to be performing much better than DOSBox defaults.

If you want to modify DOSBox settings for a game, edit `steam_dos_<appid>_<id>.conf`
file in game's installation dir. Remove it to force steam-dos to create a new one.


## Caution!

* Currently there's no Steam Cloud support

  It's recommended to disable this feature for now by unselecting:
 *Properties → Updates → Enable Steam Cloud Synchronization…*

* Do not select "DOSBox (native)" as default compatibility tool in Steam Play
  settings - it can prevent games from being installed.

## Development

Makefile default target (`lint`) runs linters on project files, use it.
Run `make install` to easily put files in Steam's `compatibilitytools.d`
directory.

Steam will detect new tool being installed after you restart the client.
As long as you don't touch .vdf files, there's no need to keep restarting
it, though.
