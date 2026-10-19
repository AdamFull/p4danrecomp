# Known issues and open questions

- **The executable and modules must be plaintext ELFs.** psvrecore reads no encrypted SELF; the version check
  refuses anything but the update 01.01's plaintext executable.
- **26 imported functions are missing** (online rankings, the game update check, the Store, and a few of libc's,
  libfios2's and libult's: [GAME_REPORT.md](GAME_REPORT.md)); none is called on the way to the menus. A call to one
  stops the program.
- **Unknown until the code is read:** where the rhythm timing comes from.
- **Linux has not been built.** It is covered only by psvrecore's CI, which runs once the repositories are pushed.
