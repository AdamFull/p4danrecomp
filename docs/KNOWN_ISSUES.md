# Known issues and open questions

- **The executable and modules must be plaintext ELFs.** psvrecore reads no encrypted SELF; the version check
  refuses anything but the update 01.01's plaintext executable.
- **26 imported functions are missing** (online rankings, the game update check, the Store, and a few of libc's,
  libfios2's and libult's: [GAME_REPORT.md](GAME_REPORT.md)); none is called on the way to the menus. A call to one
  stops the program.
- **Songs on a Pixel 8a hold the game's 30 frames a second with a few late frames** (5-12 over a song of 2:20, 6 in
  the last run, 34 of 39 five-second windows without one), since Android is told the frames' deadline (performance
  hints: its CPUs ran at about half their clocks before, and 165-219 frames were late). The Pixel 10 Pro has not been measured since
  (27.9 before). On Windows songs hold 30 at 1x, 2x and 4x (the FPS overlay, F3, shows the frame graph). What is
  left on the phones: a scene's host work (about 3.8 ms: descriptors and textures, draws, copies), writing scenes
  back under the renderer's lock (1-3 ms, now and then 8-15), and without a shader cache (the first run, or the
  first after the translator changes) the first draws of each program waiting for its pipelines: the 8a's driver
  takes 20-250 ms a graphics pipeline, so a menu or a song's start stalls for up to 1.4 s once (4.6 s before the
  secondary programs' compute shaders were made smaller; their translated fragment shaders' half-float and format
  arithmetic is most of the rest). Movie frames are converted from YUV on the GPU (0.1-0.7 ms a frame on the 8a,
  4.4-5.7 ms on the CPU before). Rendering scenes on
  a thread of their own (PSVRECORE_GXM_SCENE_THREAD=1) was slower, and P4D rewrites what a scene reads about a frame
  after it ends. The Pixel 10 Pro has no rasterization-order access (barriers before the draws that read the
  colour); it has VK_EXT_shader_tile_image and VK_KHR_dynamic_rendering_local_read, not used yet.
- **At 2x a Pixel 10 Pro runs a song at about 12 frames a second**: its GPU takes 14-21 ms a scene, four times the
  pixels of 1x (measured before the frame was shown from the GPU: the renderer now copies it into the window's image,
  where it was read back, 33 MB a frame at 4x; depth is read back and loaded a row of samples per surface row, a
  fourth of the memory at 4x). Not measured on the phones since.
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
