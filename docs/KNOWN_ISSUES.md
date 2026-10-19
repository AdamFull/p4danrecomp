# Known issues and open questions

- **The executable and modules are encrypted.** The copy of the console's files has the data in readable form,
  but `eboot.bin` and the five modules (base game and update) are encrypted SELFs: psvrecore needs them as plaintext
  ELFs, and cannot make them from these files. Until then there is no supported version, no imports and no code.
- **Unknown until the code can be analyzed:** where rhythm timing comes from, which system functions the game
  imports (how it decodes the H.264 movies and the ATRAC9 sound), and confirmation of the engine. What the data shows
  is in [GAME_REPORT.md](GAME_REPORT.md).
- **The update and the add-ons are not mounted.** The frontend mounts one folder as `app0:`; the game needs the
  update's files over the base game's there, and the add-ons under `addcont0:` (GAME_REPORT.md, "What this means for
  the runtime").
- **Linux has not been built.** It is covered only by psvrecore's CI, which runs once the repositories are pushed.
