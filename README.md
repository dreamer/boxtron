# steam-dos

Compatibility tool to run DOS games on Steam through native Linux DOSBox version.


## Prerequisites

#### Fedora

    $ sudo dnf install dosbox inotify-tools

#### Debian, Ubuntu et consortes

    $ sudo apt install dosbox inotify-tools


## Installation (using tarball)

1. Close Steam.
2. Download and unpack tarball:

        $ cd ~/.local/share/Steam/compatibilitytools.d/
        $ curl -L <latest-release-url> | tar xJf -

   TODO: update url after first release

3. Start Steam.
4. In game properties window select "Force the use of a specific Steam Play
   compatibility tool" and select "DOSBox (native)".


## Caution!


* Currently there's no Steam Overlay support
* Currently there's no Steam Cloud support

  It's recommended to disable this feature for now by unselecting:
*Properties → Updates → Enable Steam Cloud Synchronization…*

* Fullscreen DOSBox changes resolution of your display and may
  disable desktop integration (alt-tab, expose and such).
  Use alt-enter to switch to windowed mode.

* Do not select "DOSBox (native)" as default compatibility tool in Steam Play
  settings - it will prevent games from being installed.

## Development

Makefile default target (`lint`) runs linters on project files, use it.
Run `make install` to easily put files in Steam's `compatibilitytools.d`
directory.

Steam will detect new tool being installed after you restart the client.
As long as you don't touch .vdf files, there's no need to keep restarting
it, though.
