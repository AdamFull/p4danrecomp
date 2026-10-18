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

## License

MIT; see [LICENSE](LICENSE). *Persona 4: Dancing All Night* is the property of its owners and is not part of this
project.
