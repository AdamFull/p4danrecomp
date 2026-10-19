#!/usr/bin/env python3
"""Reads the game's executable (a plaintext ELF) at guest addresses, as linked: a string, or words.

    python scripts/guest_read.py <eboot.bin> <address> [--words N]
"""

import argparse
import struct
import sys


def segments(data):
    """(vaddr, file offset, file size) of each loadable segment."""
    phoff, = struct.unpack_from("<I", data, 0x1C)
    phentsize, phnum = struct.unpack_from("<HH", data, 0x2A)
    out = []
    for i in range(phnum):
        p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from("<IIIII", data, phoff + i * phentsize)
        if p_type == 1:
            out.append((p_vaddr, p_offset, p_filesz))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("elf")
    ap.add_argument("addresses", nargs="+")
    ap.add_argument("--words", type=int, default=0, help="read this many words instead of a string")
    args = ap.parse_args()
    data = open(args.elf, "rb").read()
    segs = segments(data)
    for a in args.addresses:
        address = int(a, 0)
        for vaddr, offset, size in segs:
            if vaddr <= address < vaddr + size:
                at = offset + address - vaddr
                if args.words:
                    words = struct.unpack_from(f"<{args.words}I", data, at)
                    print(f"{address:08x}: " + " ".join(f"{w:08x}" for w in words))
                else:
                    end = data.index(b"\0", at)
                    print(f"{address:08x}: {data[at:end].decode('latin-1')!r}")
                break
        else:
            print(f"{address:08x}: not in a loadable segment's file contents")
    return 0


if __name__ == "__main__":
    sys.exit(main())
