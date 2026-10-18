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
[ROADMAP.md](ROADMAP.md). Today the build compiles and tests psvrecore only.
