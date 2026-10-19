# p4danrecomp status

Each component has one of these states: **Not started** · **Implemented** · **Builds successfully** · **Tested** ·
**Integrated** · **Verified in-game**.

The toolkit's state is in [psvrecore/docs/STATUS.md](../psvrecore/docs/STATUS.md).

| Component | State | Notes |
| --- | --- | --- |
| Repository, psvrecore submodule, presets, build script | Tested (Windows) | The Windows build compiles psvrecore and runs its tests |
| Game technical report (M7, [GAME_REPORT.md](GAME_REPORT.md)) | Implemented | From the console's copy of `ux0:`: both SFOs, the update's and the add-ons' layout, save data size, the 15 CPK archives (`psvinfo cpk`), and the executable and five modules as plaintext ELFs: whole (every relocation agrees), hashed, engine (GFD) and CRI middleware versions confirmed, imports compared with psvrecore (`scripts/import_coverage.py`: 345 implemented, 204 from the game's modules, 90 missing). The rhythm timing source is left for M9 |
| Program entry (`src/main.cpp`, psvrecore's frontend) | Builds successfully (Windows, Android arm64) | The game described for the frontend: title, title ID, its code (none yet), and the version check: `eboot.bin`'s SHA-256 must be listed (the update's, from a copy of the console's folders: run on the real copy, it checks `patch/PCSB00867/eboot.bin`; `app0:` is the update over the game, `addcont0:` the add-ons), and the update 01.01's plaintext ELF is the one version listed (the base game's alone, and the encrypted SELFs, are refused). Settings, command line and window are the frontend's |
| Game configuration, overrides, patches | Not started | |
| Android application (`android/AndroidManifest.xml`, `scripts/android_apk.py`) | Tested (Pixel 10 Pro, Android 17) | psvrecore's launcher and activity with the game's `libmain.so`: installs, starts landscape, and asks for the game's folder to import. It stops at the version check after that until M7. Suspended in the background and back; on-screen controls drawn over the picture (hidden when a gamepad connects, back when the last one goes: unit-tested, not yet with a real controller); a launcher menu and a settings screen (also over the game, from the menu button or Back) |
