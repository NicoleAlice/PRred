from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import SCRIPTS, TmpRepo

SCRIPT = str(SCRIPTS / "evidence.py")


def run_in(cwd, *args, stdin=None):
    return subprocess.run(
        [sys.executable, SCRIPT] + list(args), cwd=str(cwd), capture_output=True,
        input=stdin.encode("utf-8") if stdin is not None else None,
    )


def out(res):
    return res.stdout.decode("utf-8")


def err(res):
    return res.stderr.decode("utf-8")


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.repo = TmpRepo()
        self.addCleanup(self.repo.cleanup)
        self.repo.write("a.txt", "a\n")
        self.repo.commit("init")

    def show(self, cwd=None):
        res = run_in(cwd or self.repo.dir, "show", "--json")
        self.assertEqual(res.returncode, 0, err(res))
        return json.loads(out(res))

    def add(self, text, kind="command", cwd=None):
        res = run_in(cwd or self.repo.dir, "add", "--kind", kind, "--text", text)
        self.assertEqual(res.returncode, 0, err(res))

    def test_add_then_show_not_stale(self):
        self.repo.git("branch", "-m", "dev")  # no main/master: base unresolvable
        self.add("ran tests: 12 passed")
        data = self.show()
        self.assertEqual(len(data["entries"]), 1)
        e = data["entries"][0]
        self.assertEqual(e["kind"], "command")
        self.assertEqual(e["text"], "ran tests: 12 passed")
        self.assertFalse(e["stale"])
        self.assertEqual(e["head"], data["head"])
        self.assertEqual(e["base"], "-")
        self.assertRegex(e["time"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")

    def test_base_recorded_when_resolvable(self):
        self.repo.git("checkout", "-b", "topic")
        self.repo.write("b.txt", "b\n")
        self.repo.commit("work")
        self.add("x")
        e = self.show()["entries"][0]
        self.assertRegex(e["base"], r"^[0-9a-f]{7}$")
        self.assertEqual(e["base"], self.repo.git("rev-parse", "main")[:7])

    def test_new_commit_makes_entry_stale(self):
        self.add("before")
        self.repo.write("b.txt", "b\n")
        self.repo.commit("more")
        data = self.show()
        self.assertTrue(data["entries"][0]["stale"])
        self.add("after")
        data = self.show()
        self.assertEqual([e["stale"] for e in data["entries"]], [True, False])
        res = run_in(self.repo.dir, "show")
        self.assertIn("[STALE]", out(res))

    def test_slash_branch_slug(self):
        self.repo.git("checkout", "-b", "feature/x")
        res = run_in(self.repo.dir, "path")
        self.assertEqual(res.returncode, 0, err(res))
        name = os.path.basename(out(res).strip())
        self.assertRegex(name, r"^feature-x-[0-9a-f]{6}\.md$")

    def test_two_worktrees_distinct_files(self):
        other = tempfile.mkdtemp(prefix="prready-wt-")
        self.addCleanup(lambda: __import__("shutil").rmtree(other, ignore_errors=True))
        wt = os.path.join(other, "wt")
        self.repo.git("worktree", "add", "--force", wt, "main")  # same branch twice
        p1 = out(run_in(self.repo.dir, "path")).strip()
        p2 = out(run_in(wt, "path")).strip()
        self.assertTrue(os.path.basename(p1).startswith("main-"))
        self.assertTrue(os.path.basename(p2).startswith("main-"))
        self.assertNotEqual(os.path.basename(p1), os.path.basename(p2))
        self.add("one")
        self.assertEqual(run_in(wt, "show", "--json").stdout.decode().count('"kind"'), 0)

    def test_subdirectory_uses_worktree_root(self):
        self.repo.write("sub/dir/f.txt", "x\n")
        sub = os.path.join(self.repo.dir, "sub", "dir")
        p_root = out(run_in(self.repo.dir, "path")).strip()
        p_sub = out(run_in(sub, "path")).strip()
        self.assertEqual(p_root, p_sub)
        self.add("from sub", cwd=sub)
        self.assertEqual(len(self.show()["entries"]), 1)
        self.assertFalse(os.path.exists(os.path.join(sub, ".pr-ready")))

    def test_stdin_multiline(self):
        text = "line one\n\nline three\n  indented\u00e9"
        res = run_in(self.repo.dir, "add", "--kind", "note", "--stdin", stdin=text + "\n")
        self.assertEqual(res.returncode, 0, err(res))
        self.assertEqual(self.show()["entries"][0]["text"], text)
        path = out(run_in(self.repo.dir, "path")).strip()
        with open(path, "rb") as fh:
            self.assertNotIn(b"\r", fh.read())

    def test_text_with_fake_header_lines(self):
        text = "intro\n### not a header\n### 2020-01-01 · weird\nend"
        self.add(text, kind="review")
        self.add("second")
        entries = self.show()["entries"]
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["text"], text)
        self.assertEqual(entries[1]["text"], "second")

    def test_writes_gitignore(self):
        self.add("x")
        gi = Path(self.repo.dir) / ".pr-ready" / "evidence" / ".gitignore"
        self.assertEqual(gi.read_text(encoding="utf-8").strip(), "*")
        self.assertEqual(self.repo.git("status", "--porcelain"), "")

    def test_unknown_kind_exit_2(self):
        res = run_in(self.repo.dir, "add", "--kind", "bogus", "--text", "x")
        self.assertEqual(res.returncode, 2)
        self.assertNotIn("Traceback", err(res))

    def test_text_and_stdin_exclusive_and_required(self):
        res = run_in(self.repo.dir, "add", "--kind", "note", "--text", "a", "--stdin", stdin="b")
        self.assertEqual(res.returncode, 2)
        res = run_in(self.repo.dir, "add", "--kind", "note")
        self.assertEqual(res.returncode, 2)

    def test_show_without_file(self):
        data = self.show()
        self.assertEqual(data["entries"], [])
        res = run_in(self.repo.dir, "show")
        self.assertEqual(res.returncode, 0)

    def test_not_a_repo_exit_2(self):
        d = tempfile.mkdtemp(prefix="prready-norepo-")
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        res = run_in(d, "show")
        self.assertEqual(res.returncode, 2)
        self.assertNotIn("Traceback", err(res))
        self.assertTrue(err(res).strip())

    def test_no_commits_exit_2(self):
        with TmpRepo() as empty:
            res = run_in(empty.dir, "add", "--kind", "note", "--text", "x")
            self.assertEqual(res.returncode, 2)
            self.assertNotIn("Traceback", err(res))

    def test_header_format(self):
        self.repo.git("branch", "-m", "dev")
        self.add("hello")
        path = out(run_in(self.repo.dir, "path")).strip()
        with open(path, encoding="utf-8", newline="") as fh:
            content = fh.read()
        self.assertRegex(
            content,
            r"^### \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ \u00b7 command \u00b7 head=[0-9a-f]{7} \u00b7 base=-\nhello\n\n$",
        )

    def test_non_ascii_repo_dir_with_cp1252_stdout(self):
        parent = tempfile.mkdtemp(prefix="prready-u-")
        self.addCleanup(lambda: __import__("shutil").rmtree(parent, ignore_errors=True))
        d = os.path.join(os.path.realpath(parent), "repo \u65e5\u672c")
        os.makedirs(d)
        for args in (["init", "-b", "main"], ["config", "user.name", "T"],
                     ["config", "user.email", "t@example.com"]):
            subprocess.run(["git"] + args, cwd=d, capture_output=True, check=True)
        with open(os.path.join(d, "a.txt"), "w", encoding="utf-8") as fh:
            fh.write("a\n")
        subprocess.run(["git", "add", "-A"], cwd=d, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=d, capture_output=True, check=True)
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        p = subprocess.run([sys.executable, SCRIPT, "path"], cwd=d, capture_output=True, env=env)
        self.assertEqual(p.returncode, 0, err(p))
        self.assertIn("repo \u65e5\u672c", out(p))
        a = subprocess.run([sys.executable, SCRIPT, "add", "--kind", "note", "--text", "x"],
                           cwd=d, capture_output=True, env=env)
        self.assertEqual(a.returncode, 0, err(a))
        self.assertIn("repo \u65e5\u672c", out(a))
        data = json.loads(out(run_in(d, "show", "--json")))
        self.assertEqual(len(data["entries"]), 1)

    def test_appends_newline_when_file_lacks_one(self):
        self.add("first")
        path = out(run_in(self.repo.dir, "path")).strip()
        with open(path, "rb") as fh:
            content = fh.read()
        with open(path, "wb") as fh:
            fh.write(content.rstrip(b"\n") + b"\ntrailing")
        self.add("second")
        entries = self.show()["entries"]
        self.assertEqual([e["text"] for e in entries], ["first\ntrailing", "second"])
        with open(path, "rb") as fh:
            self.assertIn(b"trailing\n### ", fh.read())


if __name__ == "__main__":
    unittest.main()
