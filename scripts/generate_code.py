#!/usr/bin/env python3
"""Recompiles the game: the update's executable and the five modules the game brings, from the game's folder (a copy
of the console's app/, patch/ and addcont/ folders, the executables as plaintext ELFs), into generated/code/<name>
with psvrecore's psvrecomp. The build then compiles them into the program (CMakeLists.txt: when generated/code is
there). Nothing it writes is committed: it is the game's code.

    python scripts/generate_code.py --game "game/<the game's folder>" [--preset windows-x64-release]
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TITLE = "PCSB00867"

# Each module: its C name, its file (from the update's folder if there, else the base game's), and where its segments
# are loaded (the executable where it is linked; the modules after it, as the runtime's loader will place them).
MODULES = [
    ("p4d_eboot", "eboot.bin", None),
    ("p4d_libc", "sce_module/libc.suprx", "0x83000000,0x83060000"),
    ("p4d_libfios2", "sce_module/libfios2.suprx", "0x83100000,0x83180000"),
    ("p4d_libult", "sce_module/libult.suprx", "0x83200000,0x83220000"),
    ("p4d_libface", "sce_module/libface.suprx", "0x83240000,0x83260000"),
    ("p4d_libsmart", "sce_module/libsmart.suprx", "0x83300000,0x83520000"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", required=True, help="the game's folder (app/, patch/, addcont/)")
    ap.add_argument("--preset", default="windows-x64-release", help="the build of psvrecomp to use")
    args = ap.parse_args()
    exe = ".exe" if sys.platform == "win32" else ""
    psvrecomp = ROOT / "build" / args.preset / "psvrecore" / "tools" / "psvrecomp" / f"psvrecomp{exe}"
    if not psvrecomp.exists():
        raise SystemExit(f"{psvrecomp} not found: build the {args.preset} preset first")
    game = Path(args.game)
    out = ROOT / "generated" / "code"
    for name, rel, bases in MODULES:
        src = game / "patch" / TITLE / rel
        if not src.exists():
            src = game / "app" / TITLE / rel
        if not src.exists():
            raise SystemExit(f"{rel}: not in {game}/patch/{TITLE} nor {game}/app/{TITLE}")
        with open(src, "rb") as f:
            if f.read(4) != b"\x7fELF":
                raise SystemExit(f"{src}: not a plaintext ELF (psvrecomp reads no encrypted SELF)")
        dest = out / name
        shutil.rmtree(dest, ignore_errors=True)
        cmd = [str(psvrecomp), "generate", str(src), str(dest), "--name", name]
        if bases:
            cmd += ["--base", bases]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            sys.stdout.write(result.stdout + result.stderr)
            raise SystemExit(f"{name}: psvrecomp failed ({result.returncode})")
        files = list(dest.glob("*.c"))
        print(f"{name}: {src.relative_to(game)} -> {len(files)} C files, {sum(p.stat().st_size for p in files) // 1024} KiB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
