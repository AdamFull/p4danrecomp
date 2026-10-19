# Game technical report (M7)

What the game's files show about Persona 4: Dancing All Night (PCSB00867, Europe). It covers only what the readable
files allow: the SFO files, the folder layout of the base game, the update and the add-ons, and the CPK archives
(read with `psvinfo cpk`). Nothing here comes from the game's code.

**Not covered yet:** the executable and its five modules are still encrypted (`psvinfo info` reports an encrypted
SELF for each). The imported system functions (NIDs), the engine's own code, the timing source of the rhythm game,
and the supported executable's hash all need the plaintext ELFs, which psvrecore cannot produce from these files.

Facts measured from the files are stated plainly. What is only suggested by names or signatures is marked
**inferred**.

## The files examined

A copy of the memory card's `ux0:` folders for the title, made on the console. The data is in readable form; the
executables are encrypted SELFs.

| Folder | Holds |
| --- | --- |
| `app/PCSB00867` | The base game: `eboot.bin`, `sce_module/` (5 modules), `data/` (2 archives, 2 icons), `sce_sys/` |
| `patch/PCSB00867` | The update: `eboot.bin`, `sce_module/` (3 modules), `data/patch.cpk`, `sce_sys/` (with `changeinfo/`) |
| `addcont/PCSB00867/<12 folders>` | The add-ons: one archive each, and `sce_sys/` |

Each `sce_sys/` also holds the console's license and package files (`package/`, `clearsign`, `keystone`). They
were not opened and are not described here.

SHA-256 of the files as supplied (encrypted SELFs). They identify the copy this report describes. They are not the
hashes the version check will use, which are those of the plaintext executable:

| File | SHA-256 |
| --- | --- |
| `app/.../eboot.bin` (2 729 936 bytes) | `a8606da7a0932d355d11c197ae9fe2180b439fc6d3d520ba3400dfa2e0a4f6ee` |
| `patch/.../eboot.bin` (2 750 592 bytes) | `2cd7e0394ab2871c5f40445bca53880ff40db80f19835b823bed689f24f0e282` |
| `app/.../sce_sys/param.sfo` | `054e985aebb57474ae0c8ed99bd64cbe1bc9796dbeca68c78a320be3019bcc57` |
| `patch/.../sce_sys/param.sfo` | `92fa760a3604b5c8869d35d9cbecc3a0d6c742a8b5919a85f47f80fffcc54560` |

## param.sfo

| Key | Base game | Update |
| --- | --- | --- |
| `TITLE` / `STITLE` | Persona 4: Dancing All Night | (same) |
| `TITLE_ID` | PCSB00867 | PCSB00867 |
| `CONTENT_ID` | EP1063-PCSB00867_00-PERSONA4D0000001 | (same) |
| `CATEGORY` | `gd` (application) | `gp` (update) |
| `APP_VER` | 01.00 | 01.01 |
| `VERSION` | 01.02 | 01.00 |
| `PSP2_SYSTEM_VER` | 0x03520000 (system software 3.52) | (same) |
| `PSP2_DISP_VER` | 03.520 | (same) |
| `PUBTOOLINFO` | `c_date=20150907,sdk_ver=03300000` | `c_date=20150922,sdk_ver=03300000` |
| `ATTRIBUTE` / `ATTRIBUTE2` / `ATTRIBUTE_MINOR` | 0x00200001 / 0 / 0x12 | (same) |
| `PARENTAL_LEVEL` | 7 | 7 |
| `REGION_DENY` | 0 | 0 |
| `SAVEDATA_MAX_SIZE` | 0x2000 (8192 KiB) | (same) |

The game was built with SDK 3.30 (`sdk_ver=03300000`) and needs system software 3.52. The update's
`changeinfo.xml` has one entry, for application version 01.01.

**Save data:** at most 8 MiB (`SAVEDATA_MAX_SIZE` counts KiB). The frontend keeps save data at
`ux0:user/00/savedata/PCSB00867` (see BUILDING.md). The save files' own layout is unknown until the game writes one.

## Update layout

The update replaces the executable and three of the five modules, and adds one archive. The others stay the base
game's:

| File | Base game | Update |
| --- | --- | --- |
| `eboot.bin` | 2 729 936 bytes | 2 750 592 bytes (replaces) |
| `sce_module/libc.suprx` | 202 560 bytes | 202 560 bytes, contents differ (replaces) |
| `sce_module/libfios2.suprx` | 116 928 bytes | 116 928 bytes (replaces) |
| `sce_module/libult.suprx` | 50 560 bytes | 50 560 bytes (replaces) |
| `sce_module/libface.suprx` | 72 208 bytes | not in the update |
| `sce_module/libsmart.suprx` | 1 574 592 bytes | not in the update |
| `data/data.cpk`, `data/vita.cpk` | 1.69 GiB, 1.42 GiB | not in the update |
| `data/patch.cpk` | — | 481 MiB (added) |

On the console, `app0:` shows the update's files over the base game's: an application started at 01.01 sees the
update's `eboot.bin`, its three modules and `data/patch.cpk`, and the base game's other files.

`patch.cpk` holds 401 files: 46 replace files of `data.cpk` (29 of those have the same extracted size), 3 replace
files of `vita.cpk`, and 352 are new (329 of them under `dance/`, 17 under `mainmenu/`). **Inferred:** the game looks
in `patch.cpk` before the base archives (the archive's name and contents suggest it; the order is in the code).

## Add-on layout

Twelve add-ons, each `addcont/PCSB00867/<name>/` with one archive `<name minus ADDCONT>.cpk` and an SFO
(`CATEGORY ac`, `CONTENT_ID EP1063-PCSB00867_00-<name>`, version 01.00). Every archive starts with an 11-byte file
`ADDCONTENTS` holding that text, a marker.

| Folder | Title (from its SFO) | Archive contents |
| --- | --- | --- |
| ADDCONTDLCD0000D | Track "Shadow World (DE DE MOUSE shadow swing mix)" | 4 note charts `dance/mns/mns029_[0-3].bin`, `movie/pv003.usm`, `sound/music/music029.{acb,awb}` |
| ADDCONTDLCD0000E | Track "Reach Out To The Truth (PERSONA MUSIC FES 2013)" | charts `mns030_*`, `pv004.usm`, `music030.*` |
| ADDCONTDLCD0000F | Track "P4 Animation Track Set A" | two songs: charts `mns037_*`, `mns038_*`; `pv008.usm`, `pv009.usm`; `music036.*`, `music037.*` |
| ADDCONTDLCD00010 | Track "P4 Animation Track Set B" | two songs: charts `mns039_*`, `mns040_*`; `pv010.usm`, `pv011.usm`; `music038.*`, `music039.*` |
| ADDCONTDLCD00013 | Track "Break Out Of..." Danced by Marie | charts `mns034_*`, `music033.*` (no movie) |
| ADDCONTDLCD00014 | Track "The Fog (ATLUS Konishi Remix)" Danced by Tohru Adachi | charts `mns035_*`, `music034.*` (no movie) |
| ADDCONTDLCF00006 | General Teddie Costume | marker only |
| ADDCONTDLCF00008 | P4G Midwinter Uniform Set | marker only |
| ADDCONTDLCF0000A | P4G Midwinter Clothes Set | marker only |
| ADDCONTDLCF0000C | P4G Ski Set | marker only |
| ADDCONTDLCF0000D | Featherman Costume Set | marker only |
| ADDCONTDLCF00011 | Featherman Mask Set | marker only |

The six costume add-ons hold no costume data: **inferred**, their presence unlocks content already in the base or
update archives. The song add-ons have four charts per song (`_0` to `_3`; **inferred:** one per difficulty) and
paths like the base game's, so **inferred:** the game reads them through the same file names once the add-on is
mounted.

## The CPK archives

All 15 archives were read with `psvinfo cpk` (psvrecore's own reader). Their tables are stored plainly (not
masked), every file is listed in a TOC (none by number only), and every file's first bytes agree with its listing:
a file whose extracted size is larger starts with `CRILAYLA` (CRI's compression), and the others do not. 0
disagreements in 7 030 files.

| Archive | Size | Files | Compressed | Extracted | Made with |
| --- | --- | --- | --- | --- | --- |
| `app/data/data.cpk` | 1 815 091 944 | 6 296 | 6 281 | 3.24 GiB | CPKFBSTD 1.49.10 |
| `app/data/vita.cpk` | 1 525 728 904 | 267 | 0 | (stored) | CPKFBSTD 1.49.10 |
| `patch/data/patch.cpk` | 504 669 536 | 401 | 385 | 604 MiB | CPKFBSTD 1.49.10 |
| 6 song add-ons | 5.3 to 66.6 MB | 7 to 15 | about half | — | CPKMC 2.48.00 |
| 6 costume add-ons | 6 272 bytes each | 1 | 0 | 11 bytes | CPKFBSTD 1.49.00 |

All use 2048-byte alignment, a TOC at 0x800 and an ETOC chunk at the end (no ITOC, no GTOC). `data.cpk`'s header
declares itself version 7, revision 13, `Sorted=1`, `EnableFileName=1`, no file CRCs.

### Contents by kind

`data.cpk` (6 296 files) and `patch.cpk` (401) hold the game's assets; `vita.cpk` (267) holds only movies and sound.

| Extension | data.cpk | patch.cpk | vita.cpk | **Inferred** meaning |
| --- | --- | --- | --- | --- |
| `GAP` | 3 884 | 239 | | Model animation packs |
| `tga` | 795 | 28 | | Textures (TGA) |
| `bin` | 576 | 3 | | Various; `dance/mns/*.bin` are note charts |
| `GFS` | 247 | 12 | | Scenes or models |
| `GMD` | 230 | 39 | | Models |
| `dds` | 199 | 46 | | Textures (DDS) |
| `bf` | 120 | | | Compiled scripts |
| `arc` | 119 | 4 | | Small archives |
| `EPL` | 65 | 8 | | Effects |
| `ENV`, `env` | 33 | 4 | | Environment (lighting) settings |
| `spr4` | 12 | 2 | | Sprites |
| `pbin` | 11 | 7 | | — |
| `GSC` | 2 | 2 | | `GFDPSP2.GSC`, `GFDPSP2PRESET.GSC` at the top: shader collections |
| `fnt` | 1 | | | Font |
| `acb` / `awb` / `acf` | 1 / 1 / 0 | 2 / 4 / 1 | 31 / 144 / 1 | CRI ADX2 cue sheets, wave banks, project settings |
| `usm` | | | 91 | CRI Sofdec movies |

Folders of `data.cpk` (files): `dance/` 4 838 (`dance/player` 4 349, `dance/camera` 131, `dance/mns` 112 charts,
`dance/ui` 83, `dance/field` 71), `mainmenu/` 630 (`mainmenu/shop_image` 563), `bustup/` 402, `event/` 120,
`sound/` 114 (`sound/lip` 112), `bg/` 100, `still/` 34, `event_cutin/` 25, `effect/` 20, and a few small ones.
`vita.cpk`: `movie/` 91 (by song, `movie/dm001/` to `movie/dm0xx/`, and 14 at the top), `sound/` 176.

### Engine

**Inferred** from the file names: the game runs on Atlus's own engine. The shader collection at the top of the
archive is named `GFDPSP2` ("PSP2" is the Vita), and the model formats (`GMD`, `GAP`, `GFS`, `EPL`) are that
engine's. This replaces the earlier PhyreEngine guess. The middleware is CRI's: File System (CPK), ADX2 (sound) and
Sofdec (movies).

### Movies

The USM movies hold H.264 video: the first one's stream is `dm001_01.264`, and its header names x264 as the
encoder. The video header lists width, height, frame rate and frame count as columns of the same @UTF tables.

### Sound

The ADX2 wave banks (`AFS2`, e.g. `sound/bgm/p4d_bgm.awb` with 510 waves) hold ATRAC9: the first wave is a RIFF file
with format tag 0xFFFE and the ATRAC9 subformat, 2 channels at 48 kHz. There are no HCA or ADX streams in it.

## What this means for the runtime

- **`app0:` is the update over the base game.** Given the copy's folder, the frontend mounts `app0:` with the
  update's files over the base game's (the executable, three modules and `patch.cpk` from the update; the rest from
  the base game), and checks the update's executable.
- **`addcont0:` holds the add-ons** (`addcont/PCSB00867/<name>`): the game lists them there and opens each with
  `sceAppUtilDrmOpen` before reading it.
- **The archives need no reader in the runtime.** The game reads them with CRI's code, through the file functions
  (or FIOS2). They are large (1.7 GiB) and read at offsets, so seeking and partial reads matter more than reading
  files whole.
- **Movies:** the runtime has an H.264 decoder (for AvPlayer). Whether the game reaches it through AvPlayer, the
  H.264 decoder library, or decodes in software is known only from its imports.
- **Sound:** ATRAC9 decoding in the runtime is needed for the music; whether through the audio decoder library or
  NGS is known only from the imports.
- **Modules:** `libface` and `libsmart` (face detection and tracking for the camera, **inferred** from the names) are
  loaded by the game; they are only in the base game.

## Still open (needs the plaintext executable)

- The executable's and modules' SHA-256 for the version check (`kVersions` in `src/main.cpp`).
- Imported libraries and functions (NIDs), and which of them psvrecore implements.
- Where the rhythm timing comes from (audio position, a clock, or frame counts).
- Confirmation of the engine, and of the inferred meanings above.
