# Known issues and open questions

- **The executable and modules must be plaintext ELFs.** psvrecore reads no encrypted SELF; the version check
  refuses anything but the update 01.01's plaintext executable.
- **90 imported functions are missing** (PSN, the system dialogs, fibers, the H.264 decoder, kernel timers, network
  initialization and a few others: [GAME_REPORT.md](GAME_REPORT.md)). A call to one stops the program.
- **The game stops after checking its add-ons** (M8): CRI AtomEx's sequencer takes a track from its pool whose
  memory has been cleared (a write to address 0x40 in `0x811c9512`, called from `0x811e0bba`; the pool's object at
  `0x83459030`, in libc's malloc heap, reads all zero). Something cleared or reused that memory while the pool still
  listed it: the runtime's sound (NGS) or threading, or another library the game relies on, behaves differently from
  the console. Being investigated.
- **Unknown until the code is read:** where the rhythm timing comes from.
- **Linux has not been built.** It is covered only by psvrecore's CI, which runs once the repositories are pushed.
