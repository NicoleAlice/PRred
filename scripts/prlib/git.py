"""Thin git helpers shared by the pr-ready scripts."""
from __future__ import annotations

import subprocess


class GitError(Exception):
    pass


def git(args, cwd):
    """Run git with an argument list; return trimmed stdout or raise GitError."""
    try:
        result = subprocess.run(
            ["git"] + list(args), cwd=str(cwd), capture_output=True,
            text=True, encoding="utf-8", errors="replace",
        )
    except OSError as exc:
        raise GitError("cannot run git: %s" % exc)
    if result.returncode != 0:
        raise GitError("git %s failed: %s" % (" ".join(args), result.stderr.strip()))
    return result.stdout.strip()


def _resolves(cwd, ref):
    try:
        git(["rev-parse", "--verify", "--quiet", ref + "^{commit}"], cwd)
        return True
    except GitError:
        return False


def resolve_base(cwd, explicit=None):
    if explicit:
        if _resolves(cwd, explicit):
            return explicit
    else:
        try:
            ref = git(["symbolic-ref", "refs/remotes/origin/HEAD"], cwd)
            prefix = "refs/remotes/"
            name = ref[len(prefix):] if ref.startswith(prefix) else ref
            if _resolves(cwd, name):
                return name
        except GitError:
            pass
        for name in ("main", "master"):
            if _resolves(cwd, name):
                return name
    raise GitError("cannot resolve base; pass --base")


def merge_base(cwd, base):
    return git(["merge-base", base, "HEAD"], cwd)


def head_sha(cwd):
    return git(["rev-parse", "HEAD"], cwd)


def current_branch(cwd):
    try:
        name = git(["symbolic-ref", "--short", "-q", "HEAD"], cwd)
    except GitError:
        return "detached"
    return name or "detached"
