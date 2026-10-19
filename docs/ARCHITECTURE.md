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
| Supplied versions | Base game package; update package A0101 (application version 01.01); 12 add-on packages (6 content, 6 unlock-only) |
| Executable hash | Unknown until the packages are decrypted (milestone M7) |
| Engine | Unknown. PhyreEngine is a candidate but has not been verified |
| Rhythm timing source | Unknown; must be found in the game code before the clock design is finalized |
