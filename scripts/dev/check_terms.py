#!/usr/bin/env python3
"""Release guard: check_terms.py TERMS_FILE

Scans every tracked file of the git repository at the current directory,
case-insensitively, for each non-empty line of TERMS_FILE, and every commit
message reachable from any ref. Prints `path:line: term` for each file hit
(line 0 means the term is in the path itself) and `commit <sha>:line: term`
for each commit-message hit (line 1 is the subject), and exits 1 on any hit, 0 when clean, 2 on a usage or environment error.

TERMS_FILE must live outside the repository and is never committed.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


class UsageError(Exception):
    pass


def _git(args, cwd):
    try:
        r = subprocess.run(["git"] + list(args), cwd=str(cwd), capture_output=True)
    except OSError as exc:
        raise UsageError("cannot run git: %s" % exc)
    if r.returncode != 0:
        raise UsageError("git %s failed: %s" % (
            " ".join(args), r.stderr.decode("utf-8", "replace").strip()))
    return r.stdout


def read_terms(path):
    try:
        with open(str(path), encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise UsageError("cannot read terms file %s: %s" % (path, exc))
    terms = [line.strip() for line in lines if line.strip()]
    if not terms:
        raise UsageError("no terms in %s" % path)
    return terms


def _inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def scan(root, terms):
    """Return (path, line, term) hits over the tracked files under root."""
    out = _git(["ls-files", "-z"], root)
    paths = [p.decode("utf-8", "replace") for p in out.split(b"\0") if p]
    lowered = [(t, t.casefold()) for t in terms]
    hits = []
    for rel in paths:
        rel_low = rel.casefold()
        for term, low in lowered:
            if low in rel_low:
                hits.append((rel, 0, term))
        try:
            data = (root / rel).read_bytes()
        except OSError:
            continue  # tracked but deleted in the worktree
        text = data.decode("utf-8", "replace")
        for n, line in enumerate(text.splitlines(), 1):
            line_low = line.casefold()
            for term, low in lowered:
                if low in line_low:
                    hits.append((rel, n, term))
    return hits


def scan_commits(root, terms):
    """Return ("commit <sha>", line, term) hits over every commit message
    reachable from any ref (line 1 is the subject)."""
    out = _git(["log", "--all", "-z", "--format=%h%x00%B", "--abbrev=12"], root)
    fields = out.decode("utf-8", "replace").split("\0")
    lowered = [(t, t.casefold()) for t in terms]
    hits = []
    for i in range(0, len(fields) - 1, 2):
        sha = fields[i].strip()
        for n, line in enumerate(fields[i + 1].splitlines(), 1):
            line_low = line.casefold()
            for term, low in lowered:
                if low in line_low:
                    hits.append(("commit " + sha, n, term))
    return hits


def main(argv):
    if len(argv) != 1:
        raise UsageError("usage: check_terms.py TERMS_FILE")
    terms_path = Path(argv[0]).resolve()
    root = Path(_git(["rev-parse", "--show-toplevel"], Path.cwd())
                .decode("utf-8").strip()).resolve()
    if _inside(terms_path, root):
        raise UsageError("the terms file must live outside the repo (%s)" % root)
    terms = read_terms(terms_path)
    hits = scan(root, terms) + scan_commits(root, terms)
    lines = ["%s:%d: %s" % hit for hit in hits]
    if hits:
        lines.append("%d hit(s) for %d term(s)" % (len(hits), len(terms)))
    else:
        lines.append("clean: %d term(s), no hits" % len(terms))
    sys.stdout.buffer.write(("\n".join(lines) + "\n").encode("utf-8"))
    return 1 if hits else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except UsageError as exc:
        sys.stderr.write("error: %s\n" % exc)
        sys.exit(2)
