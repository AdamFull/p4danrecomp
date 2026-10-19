# p4danrecomp status

Each component has one of these states: **Not started** · **Implemented** · **Builds successfully** · **Tested** ·
**Integrated** · **Verified in-game**.

The toolkit's state is in [psvrecore/docs/STATUS.md](../psvrecore/docs/STATUS.md).

| Component | State | Notes |
| --- | --- | --- |
| Repository, psvrecore submodule, presets, build script | Tested (Windows) | The Windows build compiles psvrecore and runs its tests |
| Game technical report, from the data (M7, [GAME_REPORT.md](GAME_REPORT.md)) | Implemented | From the console's copy of `ux0:`: both SFOs, the update's and the add-ons' layout, save data size, and the 15 CPK archives read with `psvinfo cpk` (engine, formats, movies H.264, sound ATRAC9) |
| Executable and modules (M7) | Not started | Blocked: the copy's `eboot.bin` and modules are encrypted SELFs, which psvrecore cannot read (see KNOWN_ISSUES). No hash, imports or timing source yet |
| Program entry (`src/main.cpp`, psvrecore's frontend) | Builds successfully (Windows, Android arm64) | The game described for the frontend: title, title ID, its code (none yet), and the version check: `eboot.bin`'s SHA-256 must be listed (the update's, from a copy of the console's folders: run on the real copy, it checks `patch/PCSB00867/eboot.bin`; `app0:` is the update over the game, `addcont0:` the add-ons), and no version is listed until M7, so every executable is refused (checked with a stand-in file; the hash agrees with Python's). Settings, command line and window are the frontend's |
| Game configuration, overrides, patches | Not started | |
| Android application (`android/AndroidManifest.xml`, `scripts/android_apk.py`) | Tested (Pixel 10 Pro, Android 17) | psvrecore's launcher and activity with the game's `libmain.so`: installs, starts landscape, and asks for the game's folder to import. It stops at the version check after that until M7. Suspended in the background and back; on-screen controls drawn over the picture; a launcher menu and a settings screen (also over the game, from the menu button or Back) |
