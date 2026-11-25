from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def run_git(args, cwd):
    result = subprocess.run(
        ["git"] + list(args), cwd=str(cwd), capture_output=True,
        text=True, encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), result.stderr))
    return result.stdout.strip()


class TmpRepo:
    """Temporary git repo on branch main; usable as a context manager."""

    def __init__(self):
        self.dir = os.path.realpath(tempfile.mkdtemp(prefix="prready-"))
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Test User")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "core.autocrlf", "false")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.cleanup()

    def cleanup(self):
        def onerror(func, path, _info):
            os.chmod(path, 0o700)
            func(path)
        shutil.rmtree(self.dir, onerror=onerror)

    def git(self, *args):
        return run_git(args, self.dir)

    def write(self, rel, content):
        path = Path(self.dir) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            with open(str(path), "w", encoding="utf-8", newline="") as fh:
                fh.write(content)
        return path

    def commit(self, msg):
        self.git("add", "-A")
        self.git("commit", "-m", msg)
        return self.git("rev-parse", "HEAD")

    def run(self, script_rel, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script_rel)] + list(args),
            cwd=self.dir, capture_output=True, text=True, encoding="utf-8",
        )
