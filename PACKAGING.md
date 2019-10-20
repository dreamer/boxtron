## Downloading the release

To obtain a source code tarball named in format `boxtron-<version>` you can
use the following URL:


    $ curl -L -O -J https://github.com/dreamer/boxtron/archive/v0.5.3.tar.gz
    …
    curl: Saved to filename 'boxtron-0.5.3.tar.gz'


## Versioning

Boxtron follows [Semantic Versioning](https://semver.org/) scheme.


## Dependencies

- Python >= 3.5
- DOSBox >= 0.74
- inotify-tools
- TiMidity++
- Fluid (R3) General MIDI SoundFont


## Installation

Use `make install` to place files in `/usr/local` hierarchy:

    $ sudo make install 
    install -m 644 -Dt "/usr/local/share/steam/compatibilitytools.d/" boxtron.vdf
    install        -Dt "/usr/local/bin/"                              install-gog-game
    install        -Dt "/usr/local/share/boxtron/"                    run-dosbox
    install -m 644 -Dt "/usr/local/share/boxtron/"                    *.py
    install -m 644 -Dt "/usr/local/share/boxtron/"                    preconfig.tar
    install -m 644 -Dt "/usr/local/share/boxtron/"                    toolmanifest.vdf
    install -m 644 -Dt "/usr/local/share/doc/boxtron/"                README.md
    install -m 644 -Dt "/usr/local/share/licenses/boxtron"            LICENSE
    
    Restart Steam, so it can pick up new compatibility tool.
    You can type "make uninstall" to remove Boxtron.


Following Makefile/environment variables affect the installation process:

- `prefix`: places files in a different hierarchy, e.g.:

      $ make prefix=/usr install

  will place the files in `/usr` instead of `/usr/local`.
  A path in file `boxtron.vdf` is derived from the value of `prefix` variable.

- `DESTDIR`: specifies root directory to put the file hierarchy in, but
  does not affect any paths inside installed files. e.g.:

      $ DESTDIR=foo make install

  will place the files in `foo/usr/local/…`.
