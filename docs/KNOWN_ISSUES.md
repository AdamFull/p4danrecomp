# Known issues and open questions

- **The executable and modules must be plaintext ELFs.** psvrecore reads no encrypted SELF; the version check
  refuses anything but the update 01.01's plaintext executable.
- **90 imported functions are missing** (PSN, the system dialogs, fibers, the H.264 decoder, kernel timers, network
  initialization and a few others: [GAME_REPORT.md](GAME_REPORT.md)). A call to one stops the program.
- **The main menu's 3D scenes are not drawn** (M8): the game renders its characters into tiled or swizzled colour
  surfaces, which psvrecore's GXM does not render yet ("scene not rendered"); the menu shows their places as flat
  shapes.
- **Unknown until the code is read:** where the rhythm timing comes from.
- **Linux has not been built.** It is covered only by psvrecore's CI, which runs once the repositories are pushed.
