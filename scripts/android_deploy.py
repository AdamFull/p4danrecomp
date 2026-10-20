#!/usr/bin/env python3
"""Builds the game for Android, installs it on the device adb sees, and puts the game's files there, ready to play:

1. the android-arm64-release preset (scripts/build.ps1 on Windows, CMake's presets elsewhere);
2. the APK (scripts/android_apk.py), debuggable so that the files can go in through run-as, installed;
3. the game's folder (game/<the game>/ with app/, patch/ and addcont/ as on the console's ux0:) copied into the
   application's internal storage on the device (files/game: adb's run-as reaches nothing else), where the
   launcher's Play finds it: only the files missing there or of another size, so a second run copies nothing.

    python scripts/android_deploy.py                         # all three
    python scripts/android_deploy.py --skip-build            # the library as built: package, install, files
    python scripts/android_deploy.py --no-files --launch     # a new build only, then start it
    python scripts/android_deploy.py --device <serial>       # one of several devices (adb devices)

Never commit or share the game's files: they stay on your computer and your device.
"""

import argparse
import os
import platform
import shlex
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRESET = "android-arm64-release"
PACKAGE = "io.github.adamfull.p4danrecomp"
LAUNCHER = "io.github.adamfull.psvrecore.LauncherActivity"
DEVICE_GAME = f"/data/user/0/{PACKAGE}/files/game"  # (internal storage: run-as reaches only that; the launcher looks there too)
PARTS = ("app", "patch", "addcont")


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def adb_cmd(device):
    return ["adb"] + (["-s", device] if device else [])


def device_shell(device, command, check=True):
    """A command line run by the device's shell (one string: the device's shell parses it)."""
    return subprocess.run(adb_cmd(device) + ["shell", command], capture_output=True, text=True, check=check).stdout


def build():
    if platform.system() == "Windows":
        run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ROOT / "scripts" / "build.ps1",
             "-Preset", PRESET, "-NoTest"])
    else:
        run(["cmake", "--preset", PRESET], cwd=ROOT)
        run(["cmake", "--build", "--preset", PRESET], cwd=ROOT)


def install(device):
    lib = ROOT / "build" / PRESET / "libmain.so"
    if not lib.exists():
        sys.exit(f"{lib} is not there: build first (without --skip-build)")
    env = dict(os.environ)
    if device:
        env["ANDROID_SERIAL"] = device  # (adb, as android_apk.py runs it)
    run([sys.executable, ROOT / "scripts" / "android_apk.py", "--debuggable", "--install"], env=env)


def local_files(game):
    """The game's files under app/, patch/ and addcont/: relative path -> (size, local path)."""
    out = {}
    for part in PARTS:
        base = game / part
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                out[path.relative_to(game).as_posix()] = (path.stat().st_size, path)
    return out


def device_files(device):
    """The files already in the application's game folder on the device: relative path -> size."""
    find = f"cd {DEVICE_GAME} 2>/dev/null && find . -type f -exec stat -c '%s %n' {{}} +"
    listing = device_shell(device, f"run-as {PACKAGE} sh -c {shlex.quote(find)}", check=False)
    out = {}
    for line in listing.splitlines():
        size, _, name = line.partition(" ")
        if size.isdigit() and name.startswith("./"):
            out[name[2:]] = int(size)
    return out


def copy_files(device, game):
    if not (game / "app").is_dir():
        sys.exit(f"{game} has no app/ folder: the game's folder is laid out as the console's ux0: "
                 "(app/<title ID>, patch/<title ID>, addcont/<title ID>)")
    have = device_files(device)
    want = local_files(game)
    send = [(rel, size, path) for rel, (size, path) in sorted(want.items()) if have.get(rel) != size]
    total = sum(size for _, size, _ in send)
    print(f"game files: {len(want)} here, {len(have)} on the device; {len(send)} to copy ({total / 2**20:.0f} MiB)")
    if not send:
        return
    # (one tar stream into the device, unpacked by the application's user: files adb pushes itself would be the
    # shell's, which the application may not read)
    unpack = f"mkdir -p {DEVICE_GAME} && tar xf - -C {DEVICE_GAME}"
    proc = subprocess.Popen(adb_cmd(device) + ["exec-in", f"run-as {PACKAGE} sh -c {shlex.quote(unpack)}"],
                            stdin=subprocess.PIPE)
    sent = 0
    with tarfile.open(fileobj=proc.stdin, mode="w|", format=tarfile.GNU_FORMAT) as tar:
        for rel, size, path in send:
            tar.add(path, arcname=rel, recursive=False)
            sent += size
            print(f"\r  {sent / 2**20:8.0f} / {total / 2**20:.0f} MiB", end="", flush=True)
    print()
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("copying the game's files failed")
    now = device_files(device)
    missing = [rel for rel, size, _ in send if now.get(rel) != size]
    if missing:
        sys.exit(f"{len(missing)} files did not arrive whole: {', '.join(missing[:5])}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--game", help="the game's folder (default: the one under game/)")
    parser.add_argument("--device", help="the device's serial (adb devices), when there are several")
    parser.add_argument("--skip-build", action="store_true", help="package and install the library as built")
    parser.add_argument("--no-install", action="store_true", help="neither build nor install: the files only")
    parser.add_argument("--no-files", action="store_true", help="leave the game's files on the device as they are")
    parser.add_argument("--launch", action="store_true", help="start the game when done")
    a = parser.parse_args()

    if not a.no_install:
        if not a.skip_build:
            build()
        install(a.device)
    if not a.no_files:
        if a.game:
            game = Path(a.game)
        else:
            folders = [p for p in (ROOT / "game").iterdir() if p.is_dir()] if (ROOT / "game").is_dir() else []
            if len(folders) != 1:
                sys.exit("say which game folder with --game (game/ holds none, or several)")
            game = folders[0]
        copy_files(a.device, game)
    if a.launch:
        run(adb_cmd(a.device) + ["shell", "am", "start", "-n", f"{PACKAGE}/{LAUNCHER}"])


if __name__ == "__main__":
    main()
