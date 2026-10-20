#!/usr/bin/env python3
"""A song's note sequence (the chart the automatic player presses from, P4D_AUTOPLAY), out of the game's data.cpk:
dance/mns/mns<song>_<difficulty>.bin (difficulty 0 easy, 1 normal, 2 hard, 3 all night), decompressed (CRILAYLA)
into generated/mns/. With --show, also its notes with their times.

    python scripts/mns_chart.py 1 1 --show

The archive's table comes from psvrecore's psvinfo (`psvinfo cpk --list`, built with the toolkit).
"""

import argparse
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANES = {0: "down", 1: "cross", 2: "left", 3: "circle", 4: "up", 5: "triangle", 8: "scratch"}


def crilayla(data):
    """A CRILAYLA-compressed file whole: the first 0x100 bytes are stored after the compressed data; the rest is
    an LZ stream read backwards, bit by bit from the end, that also fills the output from its end."""
    if data[:8] != b"CRILAYLA":
        return data
    size, header_at = struct.unpack_from("<II", data, 8)
    out = bytearray(size + 0x100)
    out[:0x100] = data[header_at + 0x10:header_at + 0x10 + 0x100]
    pos = len(data) - 0x100 - 1
    pool = left = 0

    def bits(n):
        nonlocal pos, pool, left
        value = 0
        while n:
            if left == 0:
                pool, left = data[pos], 8
                pos -= 1
            take = min(left, n)
            value = (value << take) | ((pool >> (left - take)) & ((1 << take) - 1))
            left -= take
            n -= take
        return value

    end = 0x100 + size - 1
    done = 0
    while done < size:
        if bits(1):  # (a copy of what was output before: 13 bits of distance, then the length in growing steps)
            source = end - done + bits(13) + 3
            length = 3
            for width in (2, 3, 5, 8):
                step = bits(width)
                length += step
                if step != (1 << width) - 1:
                    break
            else:
                while True:
                    step = bits(8)
                    length += step
                    if step != 0xFF:
                        break
            for _ in range(length):
                out[end - done] = out[source]
                source -= 1
                done += 1
        else:
            out[end - done] = bits(8)
            done += 1
    return bytes(out)


def find_psvinfo():
    for preset in ("windows-x64-release", "windows-x64-debug", "linux-x64-release", "linux-x64-debug"):
        for folder in (ROOT / "build" / preset / "psvrecore", ROOT / "psvrecore" / "build" / preset):
            for name in ("psvinfo.exe", "psvinfo"):
                p = folder / "tools" / "psvinfo" / name
                if p.exists():
                    return p
    sys.exit("psvinfo not found: build psvrecore (or the game) first")


def notes(chart):
    """The notes: (time in seconds, lane, raw lane word)."""
    if chart[:4] != b"MNS\0":
        sys.exit("not a note sequence (MNS)")
    bpm, = struct.unpack_from("<f", chart, 16)
    count, = struct.unpack_from("<I", chart, 28)
    for i in range(count):
        pos, lane = struct.unpack_from("<II", chart, 36 + 8 * i)
        beat = (pos >> 16) * 4 + (pos & 0x7FFF) + (0.5 if pos & 0x8000 else 0)
        yield beat * 60 / bpm, lane & 0xFF, lane


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("song", type=int)
    parser.add_argument("difficulty", type=int, choices=range(4))
    parser.add_argument("--game", default=None, help="the game folder (default: the one under game/)")
    parser.add_argument("--show", action="store_true")
    a = parser.parse_args()
    game = Path(a.game) if a.game else next((ROOT / "game").iterdir())
    cpk = game / "app" / "PCSB00867" / "data" / "data.cpk"
    name = f"dance/mns/mns{a.song:03d}_{a.difficulty}.bin"
    listing = subprocess.run([str(find_psvinfo()), "cpk", "--list", str(cpk)], capture_output=True, text=True, check=True)
    for line in listing.stdout.splitlines():
        fields = line.split("\t")
        if fields[0] == name:
            offset, stored = int(fields[2], 0), int(fields[3])
            break
    else:
        sys.exit(f"{name} is not in {cpk}")
    with open(cpk, "rb") as f:
        f.seek(offset)
        chart = crilayla(f.read(stored))
    dest = ROOT / "generated" / "mns" / Path(name).name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(chart)
    listed = list(notes(chart))
    print(f"{dest}: {len(listed)} notes, the last at {listed[-1][0]:.3f} s")
    if a.show:
        for t, lane, raw in listed:
            print(f"{t:9.3f}  {LANES.get(lane, hex(lane)):9} {raw:#x}")


if __name__ == "__main__":
    main()
