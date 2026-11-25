#!/usr/bin/env python3
"""Compare a committed generated file with a freshly generated one (CRLF-insensitive)."""
from __future__ import annotations

import argparse
import json
import sys


def first_diff_line(a, b):
    """1-based line of the first difference, or None when equal."""
    if a == b:
        return None
    la, lb = a.split(b"\n"), b.split(b"\n")
    for i in range(min(len(la), len(lb))):
        if la[i] != lb[i]:
            return i + 1
    return min(len(la), len(lb)) + 1


def compare(committed, generated):
    with open(committed, "rb") as fh:
        a = fh.read().replace(b"\r\n", b"\n")
    with open(generated, "rb") as fh:
        b = fh.read().replace(b"\r\n", b"\n")
    line = first_diff_line(a, b)
    return {"equal": line is None, "first_diff_line": line}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("committed")
    ap.add_argument("generated")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        res = compare(args.committed, args.generated)
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.json:
        text = json.dumps(res, ensure_ascii=False)
    elif res["equal"]:
        text = "equal"
    else:
        text = "differ: first difference at line %d" % res["first_diff_line"]
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    return 0 if res["equal"] else 1


if __name__ == "__main__":
    sys.exit(main())
