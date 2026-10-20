# Known issues and open questions

- **The executable and modules must be plaintext ELFs.** psvrecore reads no encrypted SELF; the version check
  refuses anything but the update 01.01's plaintext executable.
- **26 imported functions are missing** (online rankings, the game update check, the Store, and a few of libc's,
  libfios2's and libult's: [GAME_REPORT.md](GAME_REPORT.md)); none is called on the way to the menus. A call to one
  stops the program.
- **On phones the menus run just under the game's 30 frames a second**: 29-30 on a Pixel 8a, 29 on a Pixel 10 Pro
  (on Windows 30, songs and menus). Scenes are no longer waited for at their end (the CPU prepares the next while
  the GPU draws; the 8a ran the menus at 18-22 before); a scene takes about 3 ms of the CPU on the phones and 4-5 ms
  of the GPU, 3-4 of them a frame. Songs not yet measured on a phone. (Songs and menus ran at 8-17 frames a second
  on Windows too until psvrecore's texture path was fixed: hashing, decoding, the cache, render targets read as
  textures.) Measured on Windows, the frame rate falls while other heavy work runs on the machine (a build): the
  game's threads wait for the CPU.
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
