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

Put your own packages under `game/`, keeping the folders as they are:
- the base game under `Game/`;
- the update under `Updates/`;
- add-on content under `DLC/`.

Licenses and keys go in `keys/`. Both folders are git-ignored and are never modified.

The pipeline that extracts, recompiles and translates these files into `generated/` does not exist yet; see
[ROADMAP.md](ROADMAP.md).

## Running

The build makes `p4danrecomp` (`libmain.so` on Android), psvrecore's frontend with the game's code
([running a game](../psvrecore/docs/BUILDING.md#running-a-game-the-frontend)):

```
build\windows-x64-release\p4danrecomp --game <the extracted game's application folder>
```

On Android, build the android-arm64-release preset, then package and install it on the device adb sees:

```
python scripts/android_apk.py --install
```

The first start asks for the game's application folder (the system's folder picker) and copies it into the app's
folder ([Android applications](../psvrecore/docs/BUILDING.md#android-applications)).

Until the game's code is generated (M7), it refuses every executable: no version is supported yet. `run/` is
git-ignored, for a settings file (`--settings run/settings.ini`) and data (`--data run/data`) kept with the
checkout.
