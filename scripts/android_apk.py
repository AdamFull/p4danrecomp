#!/usr/bin/env python3
"""Packages the game for Android: android/AndroidManifest.xml and libmain.so (build the android-arm64-release preset
first) through psvrecore's scripts/android_apk.py. Its other options pass through (--install, --debuggable, ...).

    python scripts/android_apk.py --install
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    preset = "android-arm64-release"
    cmd = [sys.executable, str(ROOT / "psvrecore" / "scripts" / "android_apk.py"),
           "--manifest", str(ROOT / "android" / "AndroidManifest.xml"),
           "--lib", str(ROOT / "build" / preset / "libmain.so"),
           "--out", str(ROOT / "build" / preset / "p4danrecomp.apk"), *sys.argv[1:]]
    sys.exit(subprocess.run(cmd).returncode)
