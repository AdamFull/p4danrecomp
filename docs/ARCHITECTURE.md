# p4danrecomp architecture

psvrecore holds the toolkit's design: [psvrecore/docs/ARCHITECTURE.md](../psvrecore/docs/ARCHITECTURE.md). This
document covers what the game repository adds on top of it.

## Rules

- **Nothing game-specific goes into psvrecore.** This repository owns all game-specific code and data: configuration,
  function overrides, patches, timing and aspect-ratio fixes, and game settings.
- **Patches are tied to versions.** Every patch and override applies only to an executable whose SHA-256 is listed as
  supported. An unknown executable is refused, never patched.
- **Original data is preserved.** The original files in `game/` are never modified. Changes go through overrides,
  hooks or the patch layer, and replaced assets through a file-system overlay.

## Planned contents

| Part | Role |
| --- | --- |
| `config/` | Supported version hashes; analysis hints (function seeds, known jump tables); the list of allowed stubs with the reason for each |
| `src/` | Program entry and game description for psvrecore's frontend (`main.cpp`: title, title ID, code, version check), function overrides, game hooks |
| `patches/` | Patch sets, one per supported executable hash |
| `tests/` | Smoke tests and input replays covering startup, menus, entering gameplay, a full song, saving |
| `android/` | The Android application project (on-screen controls, file import, lifecycle) |

## Game facts

| | |
| --- | --- |
| Title ID | PCSB00867 (Europe, EP1063) |
| Supplied versions | Base game (application 01.00); update (01.01: executable, 3 modules, `patch.cpk`); 12 add-ons (6 songs, 6 costumes holding only a marker). See [GAME_REPORT.md](GAME_REPORT.md) |
| Executable hash | Unknown: the supplied executables are encrypted SELFs (milestone M7) |
| Engine | Atlus's own, inferred from the data (`GFDPSP2.GSC`, GMD/GAP/GFS models and animation); CRI File System, ADX2 and Sofdec. Not yet confirmed in the code |
| Rhythm timing source | Unknown; must be found in the game code before the clock design is finalized |
