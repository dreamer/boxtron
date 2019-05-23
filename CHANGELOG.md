#### 0.2.1

* Support for games, that start DOSBox via simple .bat file
  (e.g. [Worms](https://store.steampowered.com/app/70640/Worms/))
* Improve handling of empty "-c" argument - fixes many games from
  [3D Realms Classics](https://store.steampowered.com/publisher/3DREALMS/list/37610/) collection
* Fix handling of non-unicode .conf files
* Include script to simplify importing DOS games from GOG (`install-gog-game`)
* Project is now [mirrored on GitLab](https://gitlab.com/dreamer-tan/steam-dos)
* CI setup is now using [GitLab infrastructure](https://gitlab.com/dreamer-tan/steam-dos/pipelines)
* Other tiny improvements and fixes

#### 0.2.0

* MIDI support (software synthesiser starts and stops automatically with
  the game)
* Rewritten .conf generator
* Support for steam-dos settings file (`~/.config/steam-dos.conf`)
* Ability to run arbitrary executable in game directory (example:
  `SDOS_RUN_EXE=Game/SETUP.EXE %command%`)
