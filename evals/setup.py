#!/usr/bin/env python3
"""Build an eval fixture repo: setup.py SKILL CASE_ID {with,without} OUT_DIR.

Prints the runner prompt (case prompt plus the mode prefix) to stdout.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

EVALS = Path(__file__).resolve().parent
ROOT = EVALS.parent
PLUGIN_DIRS = ("skills", "scripts", "references")


class SetupError(Exception):
    pass


def load_case(skill, case_id):
    path = EVALS / skill / "cases.json"
    if not path.is_file():
        raise SetupError("no cases file for skill %r (%s)" % (skill, path))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        cases = data["cases"]
    except (ValueError, KeyError, TypeError) as exc:
        raise SetupError("malformed %s: %s" % (path, exc))
    for case in cases:
        if case.get("id") == case_id:
            return case
    ids = ", ".join(str(c.get("id")) for c in cases)
    raise SetupError("unknown case %r for %s (have: %s)" % (case_id, skill, ids))


def load_fixture(name):
    path = EVALS / "fixtures" / (name + ".py")
    if not path.is_file():
        raise SetupError("no fixture %r (%s)" % (name, path))
    # Import as part of the evals.fixtures package so relative imports work.
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location(
        "evals.fixtures." + name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "build"):
        raise SetupError("fixture %r defines no build(dir)" % name)
    return module


def plugin_root():
    # PR_READY_PLUGIN_ROOT lets tests point at a synthetic plugin tree.
    return Path(os.environ.get("PR_READY_PLUGIN_ROOT") or ROOT)


def copy_plugin(out):
    claude = out / ".claude"
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    for name in PLUGIN_DIRS:
        src = plugin_root() / name
        if src.is_dir():
            shutil.copytree(str(src), str(claude / name), ignore=ignore)
        else:
            (claude / name).mkdir(parents=True, exist_ok=True)
    exclude = out / ".git" / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    with open(str(exclude), "a", encoding="utf-8", newline="\n") as fh:
        fh.write("\n.claude/\n")


def runner_prompt(skill, mode, out, prompt):
    parts = ["Work only inside %s; it is a git repository. "
             "Do not modify anything outside it." % out,
             "The dev's answers to human gates are pre-supplied below as "
             "'dev answers: ...' lines. At a human gate, write the question you "
             "would ask the dev, then continue as if the dev gave the "
             "pre-supplied answer. If a gate comes up with no pre-supplied "
             "answer, stop there and report the question."]
    if mode == "with":
        parts.append(
            "Before starting, read %s/.claude/skills/%s/SKILL.md and follow it; "
            "its scripts and references are at %s/.claude/scripts and "
            "%s/.claude/references." % (out, skill, out, out))
    parts.append(prompt)
    return "\n\n".join(parts)


def main(argv):
    if len(argv) != 4 or argv[2] not in ("with", "without"):
        raise SetupError("usage: setup.py SKILL CASE_ID {with,without} OUT_DIR")
    skill, case_id, mode, out_arg = argv
    out = Path(out_arg).resolve()
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise SetupError("OUT_DIR %s exists and is not empty" % out)
    case = load_case(skill, case_id)
    fixture = load_fixture(case["fixture"])
    fixture.build(str(out))
    if mode == "with":
        copy_plugin(out)
    # A case may name the skill it exercises (the showcase runs pr-ready).
    target = case.get("skill") or skill
    text = runner_prompt(target, mode, str(out), case["prompt"])
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except SetupError as exc:
        sys.stderr.write("error: %s\n" % exc)
        sys.exit(2)
    except Exception as exc:  # no tracebacks for the runner
        sys.stderr.write("error: %s: %s\n" % (type(exc).__name__, exc))
        sys.exit(2)
