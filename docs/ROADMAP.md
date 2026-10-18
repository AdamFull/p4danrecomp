# p4danrecomp roadmap

The toolkit milestones M0–M6 are in [psvrecore/docs/ROADMAP.md](../psvrecore/docs/ROADMAP.md). They are verified
with test programs and do not need the game. The game milestones are:

| # | Milestone | Done when |
| --- | --- | --- |
| M7 | Decryption and extraction with psvrecore's own tools; version hashes; game technical report | Executable and modules extracted and hashed. Report covers engine, formats, imported system functions, add-on layout, save data and timing source |
| M8 | Boot through the menus | Logo, title and menus render; no unknown-function stops on that path |
| M9 | One complete song | A song plays from start to end with audio, notes and input in sync (drift measured). Saving and loading work |
| M10 | Linux parity and the Android application | Installable APK runs on a device; on-screen controls hide and show when a controller connects and disconnects |
| M11 | Enhancements and performance | Resolution, aspect ratio, anti-aliasing, FPS unlock (identical judgement timing at 30/60/120/144 fps); profiles recorded |
| M12 | Full validation | All modes, cutscenes, add-on content, long sessions; smoke tests and replays pass |

M7 can start as soon as a license for the packages is available, in parallel with the toolkit milestones.
