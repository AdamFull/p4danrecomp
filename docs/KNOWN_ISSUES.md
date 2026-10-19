# Known issues and open questions

- **The executable and modules must be plaintext ELFs.** psvrecore reads no encrypted SELF; the version check
  refuses anything but the update 01.01's plaintext executable.
- **90 imported functions are missing** (PSN, the system dialogs, fibers, the H.264 decoder, kernel timers, network
  initialization and a few others: [GAME_REPORT.md](GAME_REPORT.md)). A call to one stops the program.
- **The opening movie stays black, and streamed music is silent** (M8). Logos, the add-on check and the menus render
  and their short sounds play, but the streams starve after their first reads:
  - The opening (`movie/p4d001.usm` in vita.cpk, H.264 with ADX sound) decodes its first 22 pictures (the black
    lead-in) and the game shows them in turn; then CRI Mana reads nothing more (three reads, 338 KB of 31.5 MB) and
    the last frame stays. Its sound voice plays only zeros.
  - The menu music (ATRAC9 through NGS voices) plays 2-3 s, then CRI reports "E2011092003: Though the streamer is
    still active, voice has stopped." each server tick: the voice used its one queued buffer (the next link -1)
    before CRI queued another, though some 470 KB of the stream had been read.
  - CRI refills a voice's buffers in the NGS swap callback, and only once its stream queue holds a minimum amount
    (computed from its NGS granularity); its server, which moves stream data into that queue, runs at 30 Hz as on
    the console. The callbacks' values are as the SDK documents them. Still to find: why the queue is short when the
    voice needs it (how much the server moves per tick against what our voices consume). psvrecore's
    `PSVRECORE_WATCH`, `PSVRECORE_THREADS`, `PSVRECORE_HLE_COUNTS` and `PSVRECORE_GXM_TRACE` found this far.
  Pressing a button skips the movie.
- **Unknown until the code is read:** where the rhythm timing comes from.
- **Linux has not been built.** It is covered only by psvrecore's CI, which runs once the repositories are pushed.
