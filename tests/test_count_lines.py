from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from count_lines import count_lines  # noqa: E402
from tests.helpers import TmpRepo  # noqa: E402


def _branch(repo):
    repo.git("checkout", "-b", "feature")


class CountLinesTest(unittest.TestCase):
    def _five_line_repo(self):
        repo = TmpRepo()
        self.addCleanup(repo.cleanup)
        repo.write("app.txt", "a\nb\nc\nd\n")
        repo.commit("init")
        _branch(repo)
        repo.write("app.txt", "a\nX\nY\nZ\nd\n")  # +3 -2
        repo.commit("edit")
        return repo

    def test_counts_added_and_removed(self):
        repo = self._five_line_repo()
        res = count_lines(repo.dir)
        self.assertEqual(res["base"], "main")
        self.assertEqual(res["total"], 5)
        self.assertEqual(res["budget"], 500)
        self.assertFalse(res["over_budget"])
        f = res["files"][0]
        self.assertEqual((f["path"], f["added"], f["removed"], f["counted"]),
                         ("app.txt", 3, 2, True))

    def test_excludes_lockfile_and_generated(self):
        with TmpRepo() as repo:
            repo.write(".pr-ready/profile.md",
                       "## Generated files\n- `gen/**`\n")
            repo.write("a.txt", "x\n")
            repo.commit("init")
            _branch(repo)
            repo.write("package-lock.json", "1\n2\n3\n")
            repo.write("gen/out.js", "1\n2\n")
            repo.write("vendor/lib.c", "1\n")
            repo.write("src/real.py", "1\n")
            repo.write("notes.md", "1\n")
            repo.commit("work")
            res = count_lines(repo.dir, exclude=["*.md"])
            by = dict((f["path"], f) for f in res["files"])
            self.assertFalse(by["package-lock.json"]["counted"])
            self.assertEqual(by["package-lock.json"]["reason"], "lockfile")
            self.assertEqual(by["gen/out.js"]["reason"], "generated")
            self.assertEqual(by["vendor/lib.c"]["reason"], "vendor")
            self.assertEqual(by["notes.md"]["reason"], "excluded")
            self.assertTrue(by["src/real.py"]["counted"])
            self.assertEqual(res["total"], 1)

    def test_rename_counts_only_changed_lines(self):
        with TmpRepo() as repo:
            body = "".join("line %d\n" % i for i in range(20))
            repo.write("a.txt", body)
            repo.commit("init")
            _branch(repo)
            repo.git("mv", "a.txt", "b.txt")
            repo.write("b.txt", body.replace("line 5\n", "changed\n"))
            repo.commit("rename")
            res = count_lines(repo.dir)
            self.assertEqual(len(res["files"]), 1)
            f = res["files"][0]
            self.assertEqual((f["path"], f["added"], f["removed"]), ("b.txt", 1, 1))
            self.assertEqual(res["total"], 2)

    def test_binary_excluded(self):
        with TmpRepo() as repo:
            repo.write("a.txt", "x\n")
            repo.commit("init")
            _branch(repo)
            repo.write("img.bin", b"\x00\x01\x02\x00")
            repo.commit("bin")
            res = count_lines(repo.dir)
            f = res["files"][0]
            self.assertEqual(f["reason"], "binary")
            self.assertFalse(f["counted"])
            self.assertEqual(res["total"], 0)

    def test_handles_spaces_and_unicode(self):
        with TmpRepo() as repo:
            repo.write("a.txt", "x\n")
            repo.commit("init")
            _branch(repo)
            repo.write("docs/ação final.md", "um\ndois\n")
            repo.commit("doc")
            res = count_lines(repo.dir)
            self.assertEqual(res["files"][0]["path"], "docs/ação final.md")
            self.assertEqual(res["total"], 2)

    def test_over_budget(self):
        repo = self._five_line_repo()
        res = count_lines(repo.dir, budget=4)
        self.assertTrue(res["over_budget"])
        res = count_lines(repo.dir, budget=5)
        self.assertFalse(res["over_budget"])

    def test_profile_budget_and_warnings(self):
        repo = self._five_line_repo()
        repo.write(".pr-ready/profile.md", "## Budget\n- max_lines: nope\n")
        res = count_lines(repo.dir)
        self.assertEqual(res["budget"], 500)
        self.assertTrue(res["warnings"])

    def test_no_base_exit_2(self):
        with TmpRepo() as repo:
            repo.git("checkout", "-b", "dev")
            repo.write("a.txt", "x\n")
            repo.commit("init")
            repo.git("branch", "-m", "dev", "other")
            proc = repo.run("count_lines.py")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("cannot resolve base", proc.stderr)

    def test_os_and_value_errors_exit_2(self):
        import io
        from contextlib import redirect_stderr
        from unittest import mock

        import count_lines as cl
        for exc in (OSError("git not found"), ValueError("bad numstat")):
            buf = io.StringIO()
            with mock.patch.object(cl, "count_lines", side_effect=exc), redirect_stderr(buf):
                rc = cl.main([])
            self.assertEqual(rc, 2)
            self.assertIn(str(exc), buf.getvalue())

    def test_cli_json(self):
        repo = self._five_line_repo()
        proc = repo.run("count_lines.py", "--json", "--budget", "4")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["total"], 5)
        self.assertTrue(data["over_budget"])
        proc = repo.run("count_lines.py")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("5", proc.stdout)


if __name__ == "__main__":
    unittest.main()
