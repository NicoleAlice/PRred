from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import REPO_ROOT, run_git

SETUP = REPO_ROOT / "evals" / "setup.py"


def run_setup(*args):
    return subprocess.run(
        [sys.executable, str(SETUP)] + list(args),
        capture_output=True, text=True, encoding="utf-8",
    )


class EvalsSetupTest(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="evals-"))
        self.addCleanup(self._rm)
        self.out = os.path.join(self.tmp, "out dir")

    def _rm(self):
        def onerror(func, path, _info):
            os.chmod(path, 0o700)
            func(path)
        shutil.rmtree(self.tmp, onerror=onerror)

    def test_setup_with_copies_layout_and_builds_fixture(self):
        r = run_setup("hello", "greet", "with", self.out)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Add a one-line greeting", r.stdout)
        self.assertIn("pre-supplied answer", r.stdout)
        self.assertIn("read " + self.out, r.stdout)
        self.assertIn("Work only inside " + self.out, r.stdout)
        log = run_git(["log", "--format=%an|%ae|%s"], self.out)
        self.assertEqual(log, "Eval Dev|dev@example.com|initial")
        self.assertTrue((Path(self.out) / "README.md").is_file())
        for d in ("skills", "scripts", "references"):
            self.assertTrue((Path(self.out) / ".claude" / d).is_dir(), d)
        self.assertFalse(list(Path(self.out).rglob("__pycache__")))
        self.assertTrue((Path(self.out) / ".claude" / "scripts" / "evidence.py").is_file())
        self.assertEqual(run_git(["status", "--porcelain"], self.out), "")
        exclude = (Path(self.out) / ".git" / "info" / "exclude").read_text("utf-8")
        self.assertIn(".claude/", exclude)

    def test_setup_without_has_no_claude_dir_or_skill_prefix(self):
        r = run_setup("hello", "greet", "without", self.out)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((Path(self.out) / ".claude").exists())
        self.assertIn("Work only inside " + self.out, r.stdout)
        self.assertNotIn("SKILL.md", r.stdout)
        self.assertIn("pre-supplied answer", r.stdout)
        self.assertIn("stop there and report the question", r.stdout)

    def test_pycache_excluded_from_nested_dirs(self):
        plugin = os.path.join(self.tmp, "plugin")
        for rel in ("skills/s", "scripts/prlib/__pycache__", "references"):
            os.makedirs(os.path.join(plugin, rel))
        Path(plugin, "skills/s/SKILL.md").write_text("x")
        Path(plugin, "scripts/prlib/mod.py").write_text("x")
        Path(plugin, "scripts/prlib/__pycache__/x.pyc").write_bytes(b"\x00")
        env = dict(os.environ, PR_READY_PLUGIN_ROOT=plugin)
        r = subprocess.run(
            [sys.executable, str(SETUP), "hello", "greet", "with", self.out],
            capture_output=True, text=True, encoding="utf-8", env=env)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((Path(self.out) / ".claude/scripts/prlib/mod.py").is_file())
        self.assertFalse((Path(self.out) / ".claude/scripts/prlib/__pycache__").exists())

    def test_non_empty_out_dir_exit_2(self):
        os.makedirs(self.out)
        Path(self.out, "x").write_text("x")
        r = run_setup("hello", "greet", "without", self.out)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)

    def test_unknown_case_exit_2(self):
        r = run_setup("hello", "nope", "without", self.out)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)
        r = run_setup("nosuchskill", "greet", "without", self.out)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)

    def test_make_repo_branches_bytes_delete_dates(self):
        from evals.fixtures.lib import make_repo
        make_repo(self.out, [
            {"files": {"a.txt": "one\n", "b.bin": b"\x00\r\n"}, "commit": "c1"},
            {"branch": "feature/x", "files": {"a.txt": "two\n"},
             "delete": ["b.bin"], "commit": "c2"},
        ], remote="https://example.invalid/r.git")
        self.assertEqual(run_git(["branch", "--show-current"], self.out), "feature/x")
        self.assertEqual(run_git(["rev-parse", "main"], self.out),
                         run_git(["rev-parse", "HEAD~1"], self.out))
        self.assertEqual(
            run_git(["log", "--format=%aI|%cI", "-2"], self.out),
            "2026-01-01T00:01:00Z|2026-01-01T00:01:00Z\n"
            "2026-01-01T00:00:00Z|2026-01-01T00:00:00Z")
        self.assertFalse((Path(self.out) / "b.bin").exists())
        self.assertEqual(run_git(["remote", "get-url", "origin"], self.out),
                         "https://example.invalid/r.git")
        raw = subprocess.run(["git", "show", "main:b.bin"], cwd=self.out,
                             capture_output=True).stdout
        self.assertEqual(raw, b"\x00\r\n")


if __name__ == "__main__":
    unittest.main()
