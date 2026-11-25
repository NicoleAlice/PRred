#!/usr/bin/env python3
"""Append-only evidence log for the current branch and worktree."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prlib.git import GitError, current_branch, git, head_sha, merge_base, resolve_base  # noqa: E402

KINDS = ["command", "mutation", "review", "unverified", "note"]
SEP = "\u00b7"
HEADER_RE = re.compile(
    r"^### (\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) " + SEP + r" (" + "|".join(KINDS) + r") "
    + SEP + r" head=([0-9a-f]{7}) " + SEP + r" base=([0-9a-f]{7}|-)$"
)


class UsageError(Exception):
    pass


def _toplevel(cwd):
    return git(["rev-parse", "--show-toplevel"], cwd)


def _slug(branch):
    return re.sub(r"[^A-Za-z0-9._-]", "-", branch)


def _context(cwd):
    """Return (evidence_dir, file_path, head7, branch) for the worktree at cwd."""
    top = _toplevel(cwd)
    try:
        head = head_sha(cwd)[:7]
    except GitError:
        raise UsageError("repository has no commits yet; commit something first")
    key = os.path.realpath(top).lower()
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:6]
    edir = Path(top) / ".pr-ready" / "evidence"
    fname = "%s-%s.md" % (_slug(current_branch(cwd)), digest)
    return edir, edir / fname, head


def _base7(cwd):
    try:
        return merge_base(cwd, resolve_base(cwd))[:7]
    except GitError:
        return "-"


def _write_stdout(text):
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))


def _needs_newline(path):
    """True when the log exists, is non-empty and does not end with a newline."""
    try:
        with open(str(path), "rb") as fh:
            fh.seek(0, os.SEEK_END)
            if fh.tell() == 0:
                return False
            fh.seek(-1, os.SEEK_END)
            return fh.read(1) != b"\n"
    except FileNotFoundError:
        return False


def parse_entries(content, head):
    entries = []
    cur = None
    for line in content.replace("\r\n", "\n").split("\n"):
        m = HEADER_RE.match(line)
        if m:
            cur = {"time": m.group(1), "kind": m.group(2), "head": m.group(3),
                   "base": m.group(4), "lines": [], "stale": m.group(3) != head}
            entries.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
    for e in entries:
        e["text"] = "\n".join(e.pop("lines")).strip("\n")
    return entries


def cmd_path(args):
    _edir, path, _head = _context(".")
    _write_stdout(str(path))
    return 0


def cmd_add(args):
    if args.stdin:
        text = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    else:
        text = args.text
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    if not text.strip():
        raise UsageError("evidence text is empty")
    edir, path, head = _context(".")
    base = _base7(".")
    edir.mkdir(parents=True, exist_ok=True)
    ignore = edir / ".gitignore"
    if not ignore.exists():
        with open(str(ignore), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("*\n")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    block = "### %s %s %s %s head=%s %s base=%s\n%s\n\n" % (
        now, SEP, args.kind, SEP, head, SEP, base, text)
    if _needs_newline(path):
        block = "\n" + block
    with open(str(path), "a", encoding="utf-8", newline="\n") as fh:
        fh.write(block)
    try:  # the entry is written: a failing confirmation must not turn into exit 2
        _write_stdout("added %s entry to %s" % (args.kind, path))
    except (OSError, ValueError):
        pass
    return 0


def cmd_show(args):
    _edir, path, head = _context(".")
    entries = []
    if path.exists():
        with open(str(path), encoding="utf-8", newline="") as fh:
            entries = parse_entries(fh.read(), head)
    if args.json:
        res = {"file": str(path), "head": head, "entries": entries}
        sys.stdout.buffer.write((json.dumps(res, ensure_ascii=False) + "\n").encode("utf-8"))
        return 0
    lines = ["file: %s" % path, "head: %s" % head, "entries: %d" % len(entries)]
    for e in entries:
        lines.append("")
        lines.append("%s %s %s%s" % (e["time"], e["kind"], "head=" + e["head"],
                                     " [STALE]" if e["stale"] else ""))
        lines.append(e["text"])
    sys.stdout.buffer.write(("\n".join(lines) + "\n").encode("utf-8"))
    return 0


def build_parser():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("path", help="print the evidence file path").set_defaults(fn=cmd_path)
    add = sub.add_parser("add", help="append an entry")
    add.add_argument("--kind", required=True, choices=KINDS)
    grp = add.add_mutually_exclusive_group(required=True)
    grp.add_argument("--text")
    grp.add_argument("--stdin", action="store_true")
    add.set_defaults(fn=cmd_add)
    show = sub.add_parser("show", help="list entries")
    show.add_argument("--json", action="store_true")
    show.set_defaults(fn=cmd_show)
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)  # argparse exits 2 on usage errors
    try:
        return args.fn(args)
    except (GitError, UsageError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
