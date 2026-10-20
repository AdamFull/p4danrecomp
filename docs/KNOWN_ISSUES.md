# Known issues and open questions

- **The executable and modules must be plaintext ELFs.** psvrecore reads no encrypted SELF; the version check
  refuses anything but the update 01.01's plaintext executable.
- **26 imported functions are missing** (online rankings, the game update check, the Store, and a few of libc's,
  libfios2's and libult's: [GAME_REPORT.md](GAME_REPORT.md)); none is called on the way to the menus. A call to one
  stops the program.
- **On a Pixel 8a the menus run at 18-22 frames a second** (on Windows at the game's 30, songs and menus): a scene
  takes 11 ms there, 4.5 of them the GPU's own work and 2 more waiting for it, and the game draws 3-4 scenes a
  frame. Scenes render synchronously (each submitted and waited for before sceGxmEndScene returns), so the CPU's
  work and the GPU's never overlap; letting them is the next step. (Songs and menus ran at 8-17 frames a second on
  Windows too until psvrecore's texture path was fixed: hashing, decoding, the cache, render targets read as
  textures.)
- **A crash in Free Dance's menus on Android** (reported, not reproduced): most likely the texture cache, which grew
  by about 110 MB a second in those menus until it was bounded (8.4 GB after 75 s on Windows). Not yet checked on
  the phone with a long session.
- **Hold notes' ends are not played** by the automatic player (their length is not decoded yet): about 4 misses a
  song. The chart's lane word has flags above the lane (0x1000, 0x0400, 0x0800 on holds; 0x10000 on fever
  scratches) whose meanings are inferred, not read from the code.
- **Only one song has been played to the end** (song 1, Normal), and only by the automatic player; others, the
  other difficulties, Story Mode's dances and the add-on songs are untested.
- **The game has not been built for Linux.** psvrecore builds and passes its tests on Linux in CI; the game's own
  build and a run there need a Linux machine.
