# steam-dos

Compatibility tool to run DOS games on Steam through native Linux DOSBox version.


# Prerequisites

### Fedora

    $ sudo dnf install dosbox inotify-tools

### Debian, Ubuntu et consortes

    $ sudo apt install dosbox inotify-tools


# Installation (using tarball)

1. Close Steam.
2. Download and unpack tarball:

        $ cd ~/.local/share/Steam/compatibilitytools.d/
        $ curl -L <latest-release-url> | tar xJf -

   TODO: update url after first release

3. Start Steam.
4. In game properties window select "Force the use of a specific Steam Play
   compatibility tool" and select "DOSBox (native)".


# Caution

TODO: describe what doesn't work


# Development

Makefile default target (`lint`) runs linters on project files, use it.
Run `make install` to easily put files in Steam's `compatibilitytools.d`
directory.

Steam will detect new tool being installed after you restart the client.
As long as you don't touch .vdf files, there's no need to keep restarting
it, though.
