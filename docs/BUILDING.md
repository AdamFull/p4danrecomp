# Building p4danrecomp

The toolchain, presets and options are psvrecore's, described in
[psvrecore's docs/BUILDING.md](https://github.com/AdamFull/psvrecore/blob/master/docs/BUILDING.md). This repository uses the same preset names.

psvrecore is its own checkout, `../psvrecore` beside this repository (or the folder `PSVRECORE_ROOT` names), built
and installed once per preset into its `install/<preset>`; the game builds against that package
(psvrecore's `cmake/UsePsvrecore.cmake`). Install it again after psvrecore changes. `-DPSVRECORE_FROM_SOURCE=ON`
builds psvrecore's sources with the game instead, for changes to both at once. `psvrecore.version` holds the commit
the game was last checked with; a package from another commit gets a warning at configure time, and the game's
code may need generating again.

```
git clone --recursive https://github.com/AdamFull/psvrecore ..\psvrecore   # once, beside this repository
..\psvrecore\scripts\build.ps1 -Preset windows-x64-debug -NoTest -Install  # once per preset, and after it changes
scripts\build.ps1                                    # Windows: windows-x64-debug
scripts\build.ps1 -Preset windows-x64-release
scripts\build.ps1 -Preset android-arm64-release
```

On Linux:

```
cmake --preset linux-x64-release
cmake --build --preset linux-x64-release
ctest --preset linux-x64-release
```

## Game files

Put your own copy of the game's folders from the console under `game/`, one folder for the game holding `app/`,
`patch/` and `addcont/` as they are under `ux0:` (each with a `PCSB00867` folder): the game, the update (01.01) and
the add-ons. `game/` is git-ignored and never modified. The game's data is read as it is; its executable and modules
must be plaintext ELFs (`psvinfo info` says "container ELF").

## Recompiling the game

With psvrecore's package, recompile the game's executable and modules into `generated/code` (git-ignored: it is the
game's code), and build again: the build then compiles that code into the program.

```
scriptsuild.ps1 -Preset windows-x64-release -NoTest
python scripts/generate_code.py --game "game\<the game's folder>"
scriptsuild.ps1 -Preset windows-x64-release -NoTest -Target p4danrecomp
```

The generated C is large (about 120 MB for the executable): compiling it takes a while and a few GB of memory per
compiler. On a machine with little memory, limit the jobs (`$env:CMAKE_BUILD_PARALLEL_LEVEL = 3`).

`scripts/import_coverage.py` compares the game's imports with what psvrecore implements (after `psvinfo imports` and
`exports` have written their tables to `generated/report`, as GAME_REPORT.md describes); `scripts/guest_read.py`
reads the executable at guest addresses (strings, words), for following a crash.

## Running

The build makes `p4danrecomp` (`libmain.so` on Android), psvrecore's frontend with the game's code
([running a game](https://github.com/AdamFull/psvrecore/blob/master/docs/BUILDING.md#running-a-game-the-frontend)). On Windows and Linux it is an
executable with the game's recompiled code, on psvrecore's runtime library next to it (`psvrecore.dll`,
`libpsvrecore.so.N`, in the same build folder): the two go together, built from the same psvrecore with the same
compiler ([the shared runtime library](https://github.com/AdamFull/psvrecore/blob/master/docs/BUILDING.md#the-shared-runtime-library)); a mismatch is
refused at start-up. On Android psvrecore is linked into `libmain.so`.

```
build\windows-x64-release\p4danrecomp --game "game\<the game's folder>"
```

On Android, one script builds the android-arm64-release preset, packages and installs it (debuggable) on the device
adb sees, and copies the game's folder from `game/` into the application's internal storage. Only the files missing
there, or of another size, are copied, so a second run copies nothing. The launcher's Play then starts the game:

```
python scripts/android_deploy.py                       # build, install, copy the game's files
python scripts/android_deploy.py --skip-build --launch # the library as built; start it when done
```

`--no-files` leaves the files alone, `--no-install` copies the files only, and `--device <serial>` picks one of
several devices. Without the script, `python scripts/android_apk.py --install` packages and installs the library as
built. The first start then asks for the game's folder (the system's folder picker) and copies it into the app's
folder ([Android applications](https://github.com/AdamFull/psvrecore/blob/master/docs/BUILDING.md#android-applications)). P4D needs its update, so pick a
folder laid out as the console's ux0: (`app/`, `patch/`, `addcont/`).

Without generated code, or with an executable other than the update 01.01's plaintext ELF, it refuses to start.

### Playing a song automatically

For testing a song from start to end, an automatic player presses each note's button at its time by the game's
own clock ([src/autoplay.hpp](../src/autoplay.hpp)). Extract the song's chart from data.cpk (song 1 is
"specialist"; difficulty 0 easy, 1 normal, 2 hard, 3 all night) and point `P4D_AUTOPLAY` at it, with the press
offset in ms (about a frame early plays best: −35 at 30 frames a second):

```
python scripts/mns_chart.py 1 1
set P4D_AUTOPLAY=generated\mns\mns001_1.bin,-35
```

Then start a song (by hand, or with an `--input` script). Holds are pressed as taps; scratches flick both sticks.
`run/` is
git-ignored, for a settings file (`--settings run/settings.ini`) and data (`--data run/data`) kept with the
checkout.
