#!/usr/bin/env python3
"""Classify a change as trivial, normal or risky from the files it touches."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from count_lines import count_lines  # noqa: E402
from prlib.git import GitError  # noqa: E402
from prlib.globs import matches_any  # noqa: E402
from prlib.profile import read_profile  # noqa: E402

DEFAULT_RISK_PATHS = [
    "**/auth*/**", "**/*auth*.*", "**/*secret*", "**/*credential*",
    "**/migrations/**", "**/*.sql", ".github/workflows/**", ".gitlab-ci.yml",
    "azure-pipelines.yml", "bitbucket-pipelines.yml", "**/openapi*",
    "**/*.proto", "**/Dockerfile",
]
NON_EXECUTABLE = [
    "**/*.md", "**/*.txt", "**/*.rst", "**/*.adoc",
    "**/*.png", "**/*.jpg", "**/*.jpeg", "**/*.gif", "**/*.svg", "**/*.webp",
    "**/*.ico", "**/*.bmp", "**/LICENSE*",
]
SMALL_LINES = 10


def classify_risk(cwd, base=None):
    counted = count_lines(cwd, base)
    profile = read_profile(cwd)
    risk_paths = DEFAULT_RISK_PATHS + [
        g for g in profile["risk_paths"] if g not in DEFAULT_RISK_PATHS]
    paths = [f["path"] for f in counted["files"]]
    reasons = []
    for path in paths:
        for glob in risk_paths:
            if matches_any(path, [glob], ignore_case=True):
                reasons.append({"path": path, "rule": "risk-path:" + glob})
                break
    if reasons:
        level = "risky"
    elif paths and all(matches_any(p, NON_EXECUTABLE, ignore_case=True) for p in paths):
        level = "trivial"
    else:
        level = "normal"
    return {
        "level": level, "small": counted["total"] <= SMALL_LINES,
        "reasons": reasons, "warnings": list(counted["warnings"]),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        res = classify_risk(".", args.base)
    except (GitError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.json:
        sys.stdout.buffer.write((json.dumps(res, ensure_ascii=False) + "\n").encode("utf-8"))
    else:
        out = ["risk: %s (%s)" % (res["level"], "small" if res["small"] else "not small")]
        out += ["  %s: %s" % (r["path"], r["rule"]) for r in res["reasons"]]
        out += ["warning: " + w for w in res["warnings"]]
        sys.stdout.buffer.write(("\n".join(out) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
