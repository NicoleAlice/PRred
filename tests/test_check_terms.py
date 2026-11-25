from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from tests.helpers import SCRIPTS, TmpRepo

CHECK = SCRIPTS / "dev" / "check_terms.py"


class CheckTermsTest(unittest.TestCase):
    def setUp(self):
        self.repo = TmpRepo()
        self.addCleanup(self.repo.cleanup)
        outside = tempfile.mkdtemp(prefix="prready-terms-")
        self.addCleanup(shutil.rmtree, outside, True)
        self.terms = os.path.join(outside, "terms.txt")

    def write_terms(self, text):
        with open(self.terms, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)

    def run_check(self, *args):
        return subprocess.run(
            [sys.executable, str(CHECK)] + list(args), cwd=self.repo.dir,
            capture_output=True, text=True, encoding="utf-8")

    def test_check_terms_finds_planted_term_exit_1_and_clean_exit_0(self):
        self.write_terms("Plugh\n\n  xyzzy  \n")
        self.repo.write("README.md", "# demo\n\nNothing here.\n")
        self.repo.write("docs/notes.md", "line one\nWe used the PLUGH build.\n")
        self.repo.write("untracked.txt", "plugh\n")
        self.repo.git("add", "README.md", "docs/notes.md")
        self.repo.git("commit", "-m", "init")

        r = self.run_check(self.terms)
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("docs/notes.md:2: Plugh", r.stdout)
        self.assertNotIn("untracked.txt", r.stdout)
        self.assertNotIn("README.md", r.stdout)

        self.repo.write("docs/notes.md", "line one\nWe used the plain build.\n")
        self.repo.git("add", "docs/notes.md")
        self.repo.git("commit", "-m", "clean")
        r = self.run_check(self.terms)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("Plugh", r.stdout)

    def test_hit_in_path_and_unicode_spaces(self):
        self.write_terms("xyzzy\n")
        self.repo.write("docs/xyzzy plan.md", "ok\n")
        self.repo.write("café/nota.md", "Antes\nfeito na Xyzzy\n")
        self.repo.commit("init")
        r = self.run_check(self.terms)
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("docs/xyzzy plan.md:0: xyzzy", r.stdout)
        self.assertIn("café/nota.md:2: xyzzy", r.stdout)

    def test_hit_in_commit_message_subject_and_body_on_any_branch(self):
        self.write_terms("xyzzy\n")
        self.repo.write("README.md", "clean\n")
        self.repo.commit("init")
        self.repo.write("a.txt", "a\n")
        self.repo.commit("Fix login\n\nSame bug we saw at Xyzzy.")
        sha = self.repo.git("rev-parse", "--short=12", "HEAD").strip()
        self.repo.git("checkout", "-q", "-b", "side")
        self.repo.write("b.txt", "b\n")
        self.repo.commit("XYZZY port")
        side = self.repo.git("rev-parse", "--short=12", "HEAD").strip()
        self.repo.git("checkout", "-q", "-")
        r = self.run_check(self.terms)
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("commit %s:3: xyzzy" % sha, r.stdout)
        self.assertIn("commit %s:1: xyzzy" % side, r.stdout)
        self.assertNotIn("README.md", r.stdout)
        self.assertEqual(r.stdout.count("commit "), 2, r.stdout)

    def test_hit_in_root_commit_message(self):
        self.write_terms("xyzzy\n")
        self.repo.write("README.md", "clean\n")
        self.repo.commit("Import from xyzzy")
        root = self.repo.git("rev-parse", "--short=12", "HEAD")
        self.repo.write("a.txt", "a\n")
        self.repo.commit("second")
        r = self.run_check(self.terms)
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("commit %s:1: xyzzy" % root, r.stdout)

    def test_clean_files_and_history_exit_0(self):
        self.write_terms("xyzzy\n")
        self.repo.write("README.md", "clean\n")
        self.repo.commit("init\n\nnothing to see")
        r = self.run_check(self.terms)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("clean", r.stdout)

    def test_binary_file_does_not_crash(self):
        self.write_terms("xyzzy\n")
        self.repo.write("img.bin", b"\x00\xff\xfeXYZZY\x00")
        self.repo.commit("init")
        r = self.run_check(self.terms)
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("img.bin:1: xyzzy", r.stdout)

    def test_usage_errors_exit_2(self):
        self.repo.write("README.md", "x\n")
        self.repo.commit("init")
        r = self.run_check()
        self.assertEqual(r.returncode, 2)
        self.assertIn("usage", r.stderr)
        r = self.run_check(os.path.join(os.path.dirname(self.terms), "missing.txt"))
        self.assertEqual(r.returncode, 2)
        self.write_terms("\n   \n")
        r = self.run_check(self.terms)
        self.assertEqual(r.returncode, 2)
        self.assertIn("no terms", r.stderr)

    def test_terms_file_inside_repo_exit_2(self):
        self.repo.write("README.md", "x\n")
        self.repo.commit("init")
        inside = self.repo.write("terms.txt", "secretco\n")
        r = self.run_check(str(inside))
        self.assertEqual(r.returncode, 2)
        self.assertIn("outside the repo", r.stderr)


if __name__ == "__main__":
    unittest.main()
