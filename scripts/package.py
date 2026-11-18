#!/usr/bin/env python3
"""Generates, builds and packages the game for one platform, named and iconed from the game's own sce_sys (title,
translations, title ID and version from param.sfo; icon0.png, or game/icon.png when you put one there), with
psvrecore's scripts/package.py (its description has the steps and options):

    python scripts/package.py windows   # build/package/windows/p4danrecomp/ (and install.ps1: a Start menu shortcut)
    python scripts/package.py linux     # build/package/linux/p4danrecomp/ (.desktop entry, icons, install.sh)
    python scripts/package.py android   # build/package/android/p4danrecomp.apk

The game's folder is the one in game/ (or --game <folder>). The pictures and files made from sce_sys go to
generated/package/; nothing made from the game is committed.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    sys.exit(subprocess.run([sys.executable, str(ROOT / "psvrecore" / "scripts" / "package.py"), *sys.argv[1:],
                             "--root", str(ROOT), "--name", "p4danrecomp"]).returncode)
