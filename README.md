# p4danrecomp

A native port of *Persona 4: Dancing All Night* (PS Vita) to Windows, Linux and Android. It works by static
recompilation:
- the game's executable code is translated ahead of time into C and compiled with Clang;
- it runs on [psvrecore](https://github.com/AdamFull/psvrecore), a reusable PS Vita recompilation toolkit, included
  here as a git submodule.

This repository holds only what is specific to the game: its configuration, integration, patches, fixes and
settings.

**This repository contains no game code, assets, keys or SDK material.** You supply your own copy of the game and DLC.
Everything derived from it (decrypted files, recompiled sources, translated shaders) is generated on your machine
under `generated/` and never committed.

Status: early setup. Nothing runs yet. See [docs/STATUS.md](docs/STATUS.md).

## Layout

| Folder | Contents |
| --- | --- |
| `psvrecore` | The toolkit (submodule) |
| `game` | Your original game packages (git-ignored, never modified) |
| `keys` | Licenses and keys you supply (git-ignored) |
| `generated` | Extracted, recompiled and translated output (git-ignored) |
| `scripts` | Build helpers |
| `docs` | [Architecture](docs/ARCHITECTURE.md) · [Roadmap](docs/ROADMAP.md) · [Status](docs/STATUS.md) · [Known issues](docs/KNOWN_ISSUES.md) · [Building](docs/BUILDING.md) |

## Building

```
git submodule update --init --recursive
scripts\build.ps1
```

See [docs/BUILDING.md](docs/BUILDING.md).

## Packaging

One command per platform builds the game from its folder in `game/` (recompiling it first when `generated/code` is
empty) and packages it, named and iconed from the game's own `sce_sys` (`param.sfo`'s title, translations and
version; `icon0.png`, or `game/icon.png` when you put a logo there):

```
python scripts/package.py windows   # build/package/windows/p4danrecomp/ (install.ps1 adds a Start menu shortcut)
python scripts/package.py linux     # build/package/linux/p4danrecomp/ (on Linux: .desktop entry, icons, install.sh)
python scripts/package.py android   # build/package/android/p4danrecomp.apk (--install installs it)
```

What is made from `sce_sys` goes to `generated/package/`; nothing made from the game is committed. Details:
psvrecore's [docs/BUILDING.md](psvrecore/docs/BUILDING.md), "Packaging a game".

## License

MIT; see [LICENSE](LICENSE). *Persona 4: Dancing All Night* is the property of its owners and is not part of this
project.
