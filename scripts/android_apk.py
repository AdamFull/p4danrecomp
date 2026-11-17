#!/usr/bin/env python3
"""Packages the game for Android: android/AndroidManifest.xml and libmain.so (build the android-arm64-release preset
first) through psvrecore's scripts/android_apk.py. Its other options pass through (--install, --debuggable, ...).

The launcher icon is made from a picture on this computer, never kept in the repository: game/icon.png when you put
one there, otherwise the game's own icon (game/<the game>/app/PCSB00867/sce_sys/icon0.png). Without either, the
package gets a plain placeholder.

    python scripts/android_apk.py --install
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TITLE_ID = "PCSB00867"


def icon_picture():
    game = ROOT / "game"
    if (game / "icon.png").is_file():
        return game / "icon.png"
    found = sorted(game.glob(f"*/app/{TITLE_ID}/sce_sys/icon0.png")) if game.is_dir() else []
    return found[0] if found else None


if __name__ == "__main__":
    preset = "android-arm64-release"
    cmd = [sys.executable, str(ROOT / "psvrecore" / "scripts" / "android_apk.py"),
           "--manifest", str(ROOT / "android" / "AndroidManifest.xml"),
           "--lib", str(ROOT / "build" / preset / "libmain.so"),
           "--out", str(ROOT / "build" / preset / "p4danrecomp.apk")]
    picture = icon_picture()
    if picture and "--icon" not in sys.argv:
        print(f"icon: {picture}")
        cmd += ["--icon", str(picture)]
    elif not picture:
        print("icon: no game/icon.png, nor the game's icon0.png under game/: a placeholder")
    sys.exit(subprocess.run(cmd + sys.argv[1:]).returncode)
