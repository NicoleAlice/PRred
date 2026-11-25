#!/usr/bin/env python3
"""Count build warnings in two logs and report the ones the branch added.

Exits 1 when the branch log has any warning the base log lacks (new unique
warnings), even if the total went down; `delta` is information only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
PROJECT_SUFFIX = re.compile(r"\s*\[[^\[\]]*\]\s*$")


def _root_regex(roots):
    variants = set()
    for root in roots:
        root = root.rstrip("/\\")
        if not root:
            continue
        variants.add(root)
        variants.add(root.replace("\\", "/"))
        variants.add(root.replace("/", "\\"))
    if not variants:
        return None
    ordered = sorted(variants, key=len, reverse=True)
    return re.compile("(?:" + "|".join(re.escape(v) for v in ordered) + ")[/" + chr(92) * 2 + "]?")


def normalize(line, root_re):
    line = ANSI.sub("", line)
    if root_re is not None:
        line = root_re.sub("", line)
    line = PROJECT_SUFFIX.sub("", line)
    return " ".join(line.split())


def warnings_in(path, pattern, root_re):
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8", errors="replace")
    found = set()
    for raw in text.splitlines():
        line = normalize(raw, root_re)
        if line and pattern.search(line):
            found.add(line)
    return found


def warning_delta(base_log, branch_log, pattern=r"\bwarning\b", roots=()):
    pat = re.compile(pattern, re.IGNORECASE)
    root_re = _root_regex(roots)
    base = warnings_in(base_log, pat, root_re)
    branch = warnings_in(branch_log, pat, root_re)
    return {"base": len(base), "branch": len(branch),
            "delta": len(branch) - len(base), "added": sorted(branch - base)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("base_log")
    ap.add_argument("branch_log")
    ap.add_argument("--pattern", default=r"\bwarning\b")
    ap.add_argument("--root", action="append", default=[])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        res = warning_delta(args.base_log, args.branch_log, args.pattern, args.root)
    except (OSError, re.error) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.json:
        text = json.dumps(res, ensure_ascii=False)
    else:
        lines = ["warnings: base %d, branch %d, delta %+d"
                 % (res["base"], res["branch"], res["delta"])]
        lines += ["  + " + w for w in res["added"]]
        text = "\n".join(lines)
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    return 1 if res["added"] else 0  # new unique warnings fail even if delta <= 0


if __name__ == "__main__":
    sys.exit(main())
