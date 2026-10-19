#!/usr/bin/env python3
"""Which of the game's imported functions are there when it runs: implemented by psvrecore's HLE libraries (an
HLE_FUNCTION in its sources), exported by a module the game brings and that is recompiled with it (libc, libfios2,
libult, libface, libsmart), or missing. Reads the tables psvinfo writes (generated/report/imports_*.tsv and
exports_*.tsv) and writes generated/report/coverage.tsv; prints a summary by library.

    python scripts/import_coverage.py
"""

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "generated" / "report"


def hle_nids():
    """The NIDs psvrecore's HLE libraries implement: every HLE_FUNCTION in its sources, and the functions and
    variables listed by hand ({0x..., "name", ...} or Function{0x..., "name", ...})."""
    found = set()
    for path in (ROOT / "psvrecore" / "libs").rglob("*.cpp"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'HLE_\w+\(\s*0x([0-9A-Fa-f]{8})|\{\s*0x([0-9A-Fa-f]{8}),\s*"\w+"', text):
            found.add(int(m.group(1) or m.group(2), 16))
    return found


def table(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main():
    hle = hle_nids()
    exported = {}
    for path in REPORT.glob("exports_*.tsv"):
        module = path.stem[len("exports_"):]
        for row in table(path):
            exported[(int(row["library_nid"], 16), int(row["nid"], 16))] = module
    rows = []
    summary = defaultdict(lambda: defaultdict(int))
    for path in sorted(REPORT.glob("imports_*.tsv")):
        importer = path.stem[len("imports_"):]
        for row in table(path):
            lib, nid = int(row["library_nid"], 16), int(row["nid"], 16)
            if (lib, nid) in exported:
                where = "module:" + exported[(lib, nid)]
            elif nid in hle:
                where = "hle"
            else:
                where = "missing"
            rows.append([importer, row["library"], row["kind"], row["nid"], row["name"], where])
            summary[(importer, row["library"])][where.split(":")[0]] += 1
    with open(REPORT / "coverage.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["importer", "library", "kind", "nid", "name", "provided_by"])
        w.writerows(rows)
    total = defaultdict(int)
    print(f"{'importer':<10} {'library':<26} {'hle':>4} {'module':>6} {'missing':>7}")
    for (importer, lib), c in sorted(summary.items()):
        print(f"{importer:<10} {lib:<26} {c['hle']:>4} {c['module']:>6} {c['missing']:>7}")
        for k, v in c.items():
            total[k] += v
    print(f"total: {total['hle']} HLE, {total['module']} from modules, {total['missing']} missing")


if __name__ == "__main__":
    sys.exit(main())
