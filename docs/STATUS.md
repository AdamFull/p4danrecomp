# p4danrecomp status

Each component has one of these states: **Not started** · **Implemented** · **Builds successfully** · **Tested** ·
**Integrated** · **Verified in-game**.

The toolkit's state is in [psvrecore/docs/STATUS.md](../psvrecore/docs/STATUS.md).

| Component | State | Notes |
| --- | --- | --- |
| Repository, psvrecore submodule, presets, build script | Tested (Windows) | The Windows build compiles psvrecore and runs its tests |
| Game decryption and extraction (M7) | Not started | Blocked: no license for the packages yet (see KNOWN_ISSUES) |
| Program entry (`src/main.cpp`, psvrecore's frontend) | Builds successfully (Windows, Android arm64) | The game described for the frontend: title, title ID, its code (none yet), and the version check: `eboot.bin`'s SHA-256 must be listed, and no version is listed until M7, so every executable is refused (checked with a stand-in file; the hash agrees with Python's). Settings, command line and window are the frontend's |
| Game configuration, overrides, patches | Not started | |
| Android application (`android/AndroidManifest.xml`, `scripts/android_apk.py`) | Tested (Pixel 10 Pro, Android 17) | psvrecore's launcher and activity with the game's `libmain.so`: installs, starts landscape, and asks for the game's folder to import. It stops at the version check after that until M7. On-screen controls and a settings screen are not there |
