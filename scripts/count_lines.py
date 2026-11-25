#!/usr/bin/env python3
"""Count hand-written changed lines (added + removed) against the merge-base."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prlib.git import GitError, git, merge_base, resolve_base  # noqa: E402
from prlib.globs import matches_any  # noqa: E402
from prlib.profile import read_profile  # noqa: E402

LOCKFILES = [
    "**/package-lock.json", "**/pnpm-lock.yaml", "**/yarn.lock", "**/*.lock",
    "**/go.sum", "**/packages.lock.json", "**/poetry.lock", "**/composer.lock",
]
VENDOR = ["vendor/**", "**/node_modules/**", "third_party/**"]
DEFAULT_EXCLUDES = LOCKFILES + VENDOR


def _parse_numstat(raw):
    """Parse `git diff --numstat -z -M` output into (added, removed, path, binary)."""
    parts = raw.split("\0")
    entries = []
    i = 0
    while i < len(parts):
        rec = parts[i]
        i += 1
        if not rec:
            continue
        fields = rec.split("\t", 2)
        if len(fields) < 3:
            continue
        added, removed, path = fields
        if path == "":  # rename/copy: old and new paths follow as separate records
            if i + 1 >= len(parts):
                break
            path = parts[i + 1]
            i += 2
        binary = added == "-" and removed == "-"
        entries.append((0 if binary else int(added), 0 if binary else int(removed),
                        path, binary))
    return entries


def count_lines(cwd, base=None, exclude=None, budget=None):
    base = resolve_base(cwd, base)
    mb = merge_base(cwd, base)
    profile = read_profile(cwd)
    if budget is None:
        budget = profile["budget"]
    exclude = list(exclude or [])
    raw = git(["diff", "--numstat", "-z", "-M", mb, "HEAD"], cwd)
    files = []
    total = 0
    for added, removed, path, binary in _parse_numstat(raw):
        reason = None
        if binary:
            reason = "binary"
        elif exclude and matches_any(path, exclude):
            reason = "excluded"
        elif matches_any(path, profile["generated"]):
            reason = "generated"
        elif matches_any(path, LOCKFILES):
            reason = "lockfile"
        elif matches_any(path, VENDOR):
            reason = "vendor"
        entry = {"path": path, "added": added, "removed": removed,
                 "counted": reason is None}
        if reason:
            entry["reason"] = reason
        else:
            total += added + removed
        files.append(entry)
    return {
        "base": base, "merge_base": mb, "total": total, "budget": budget,
        "over_budget": total > budget, "files": files,
        "warnings": list(profile["warnings"]),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base")
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--budget", type=int)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        res = count_lines(".", args.base, args.exclude, args.budget)
    except (GitError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.json:
        sys.stdout.buffer.write((json.dumps(res, ensure_ascii=False) + "\n").encode("utf-8"))
    else:
        out = ["%d hand-written lines vs budget %d (%s) against %s"
               % (res["total"], res["budget"],
                  "OVER" if res["over_budget"] else "ok", res["base"])]
        for f in res["files"]:
            if not f["counted"]:
                out.append("  skipped %s (%s)" % (f["path"], f["reason"]))
        out += ["warning: " + w for w in res["warnings"]]
        sys.stdout.buffer.write(("\n".join(out) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
