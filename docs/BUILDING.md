# Building p4danrecomp

The toolchain, presets and options are psvrecore's, described in
[psvrecore/docs/BUILDING.md](../psvrecore/docs/BUILDING.md). This repository uses the same preset names.

```
git submodule update --init --recursive
scripts\build.ps1                                    # Windows: windows-x64-debug, build + tests
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

Build once (for psvrecomp), recompile the game's executable and modules into `generated/code` (git-ignored: it is the
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
([running a game](../psvrecore/docs/BUILDING.md#running-a-game-the-frontend)):

```
build\windows-x64-release\p4danrecomp --game "game\<the game's folder>"
```

On Android, build the android-arm64-release preset, then package and install it on the device adb sees:

```
python scripts/android_apk.py --install
```

The first start asks for the game's application folder (the system's folder picker) and copies it into the app's
folder ([Android applications](../psvrecore/docs/BUILDING.md#android-applications)).

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
