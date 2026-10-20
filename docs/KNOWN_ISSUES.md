# Known issues and open questions

- **The executable and modules must be plaintext ELFs.** psvrecore reads no encrypted SELF; the version check
  refuses anything but the update 01.01's plaintext executable.
- **26 imported functions are missing** (online rankings, the game update check, the Store, and a few of libc's,
  libfios2's and libult's: [GAME_REPORT.md](GAME_REPORT.md)); none is called on the way to the menus. A call to one
  stops the program.
- **Songs on phones run just under the game's 30 frames a second, with a late frame (67 ms) in most five-second
  windows**: 29.3 on a Pixel 8a (105 late frames over the song and its menus), 27.9 on a Pixel 10 Pro (measured before
  the CPU lending below). On Windows songs hold 30 at 1x, 2x and 4x (a late frame in 1-2 of 19 windows; the FPS
  overlay, F3, shows the frame graph). On the phones the game's three emulated CPUs are what run out: in a late
  frame its threads held about 175 of their 200 ms, a scene's host work 4 ms of it (copies of vertices and
  uniforms, textures, commands; vertex streams are copied once a scene now, straight into their buffer), and the
  game's job threads waited for a CPU. A scene's end now lends its CPU to them while the host renders (164 late
  frames to 105 on the 8a). Rendering scenes on a thread of their own (PSVRECORE_GXM_SCENE_THREAD=1) was slower, and
  P4D rewrites what a scene reads about a frame after it ends, so that thread stays at most a scene behind. The GPU
  takes 3.7-5.5 ms a scene (4-5 scenes a frame); the Pixel 10 Pro has no rasterization-order access (barriers
  before the 26-32 draws a scene that read the colour; it has VK_EXT_shader_tile_image and
  VK_KHR_dynamic_rendering_local_read, not used yet).
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
