"""Deterministic git fixture builder shared by all eval fixtures."""
from __future__ import annotations

import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE_TIME = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


def _git(args, cwd, env=None):
    result = subprocess.run(
        ["git"] + list(args), cwd=str(cwd), capture_output=True,
        text=True, encoding="utf-8", env=env,
    )
    if result.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), result.stderr.strip()))
    return result.stdout


def _branch_exists(name, cwd):
    r = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", "refs/heads/" + name],
        cwd=str(cwd), capture_output=True,
    )
    return r.returncode == 0


def make_repo(dir, steps, remote=None):
    """Create a repo in `dir` (branch main) by replaying `steps`.

    Step keys: "files" {rel: str|bytes}, "delete" [rel], "commit" msg (required),
    "branch" name (checked out, created if needed, before writing).
    """
    root = Path(dir)
    root.mkdir(parents=True, exist_ok=True)
    _git(["init", "-b", "main"], root)
    _git(["config", "user.name", "Eval Dev"], root)
    _git(["config", "user.email", "dev@example.com"], root)
    _git(["config", "core.autocrlf", "false"], root)
    if remote:
        _git(["remote", "add", "origin", remote], root)
    for i, step in enumerate(steps):
        if "commit" not in step:
            raise ValueError("step %d has no 'commit'" % i)
        branch = step.get("branch")
        if branch:
            if _branch_exists(branch, root):
                _git(["checkout", branch], root)
            else:
                _git(["checkout", "-b", branch], root)
        for rel, content in (step.get("files") or {}).items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, bytes):
                path.write_bytes(content)
            else:
                with open(str(path), "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(content)
        for rel in step.get("delete") or []:
            target = root / rel
            if target.exists():
                target.unlink()
        stamp = (BASE_TIME + timedelta(minutes=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        env = dict(os.environ, GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
        _git(["add", "-A"], root, env)
        _git(["commit", "--allow-empty", "-m", step["commit"]], root, env)
