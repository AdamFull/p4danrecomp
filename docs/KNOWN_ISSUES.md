# Known issues and open questions

- **The executable and modules must be plaintext ELFs.** psvrecore reads no encrypted SELF; the version check
  refuses anything but the update 01.01's plaintext executable.
- **26 imported functions are missing** (online rankings, the game update check, the Store, and a few of libc's,
  libfios2's and libult's: [GAME_REPORT.md](GAME_REPORT.md)); none is called on the way to the menus. A call to one
  stops the program.
- **Songs ran at 11-17 frames a second** until psvrecore's texture hashing and 8-bit texture decoding were made
  faster: now at the game's 30 (a scene 6.5 ms, from 37; `PSVRECORE_GXM_PROFILE=1` shows where a scene's time
  goes). Scenes still render synchronously, the GPU waited for at each (about 3 ms of the 6.5).
- **Hold notes' ends are not played** by the automatic player (their length is not decoded yet): about 4 misses a
  song. The chart's lane word has flags above the lane (0x1000, 0x0400, 0x0800 on holds; 0x10000 on fever
  scratches) whose meanings are inferred, not read from the code.
- **Only one song has been played to the end** (song 1, Normal), and only by the automatic player; others, the
  other difficulties, Story Mode's dances and the add-on songs are untested.
- **The game has not been built for Linux.** psvrecore builds and passes its tests on Linux in CI; the game's own
  build and a run there need a Linux machine.
