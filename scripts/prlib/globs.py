"""Glob matching with ** support (no stdlib equivalent before 3.13)."""
from __future__ import annotations

import re


def glob_to_regex(glob, ignore_case=False):
    glob = glob.replace("\\", "/")
    out = []
    i = 0
    n = len(glob)
    while i < n:
        c = glob[i]
        if c == "*":
            if glob.startswith("**", i):
                j = i + 2
                if glob.startswith("/", j):
                    out.append("(?:.*/)?")  # zero or more directories
                    i = j + 1
                else:
                    out.append(".*")
                    i = j
            else:
                out.append("[^/]*")
                i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(c))
            i += 1
    flags = re.IGNORECASE if ignore_case else 0
    return re.compile("^" + "".join(out) + "$", flags)


def matches_any(path, globs, ignore_case=False):
    path = path.replace("\\", "/")
    return any(glob_to_regex(g, ignore_case).match(path) for g in globs)
