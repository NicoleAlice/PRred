from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "warning_delta.py"


class WarningDeltaTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def _run(self, base, branch, *extra):
        pa = self.dir / "base.log"
        pb = self.dir / "branch.log"
        pa.write_bytes(base)
        pb.write_bytes(branch)
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(pa), str(pb), "--json"] + list(extra),
            capture_output=True)

    def test_same_warnings_different_roots_delta_0(self):
        base = rb"C:\work\a\src/Foo.cs(3,4): warning CS0168: unused  [C:\work\a\p.csproj]" + b"\n"
        branch = rb"D:/other/b/src/Foo.cs(3,4): warning CS0168: unused [D:\other\b\p.csproj]" + b"\n"
        r = self._run(base, branch, "--root", r"C:\work\a", "--root", r"D:\other\b")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout),
                         {"base": 1, "branch": 1, "delta": 0, "added": []})

    def test_new_warning_delta_1_exit_1_listed(self):
        base = b"\x1b[33mwarning: old thing\x1b[0m\nok line\n"
        branch = b"warning: old thing\nWARNING: brand new\n"
        r = self._run(base, branch)
        self.assertEqual(r.returncode, 1)
        res = json.loads(r.stdout)
        self.assertEqual((res["base"], res["branch"], res["delta"]), (1, 2, 1))
        self.assertEqual(res["added"], ["WARNING: brand new"])

    def test_duplicates_counted_once(self):
        r = self._run(b"warning: a\n", b"warning: a\nwarning:   a\nwarning: a\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["branch"], 1)

    def test_project_suffix_stripped(self):
        r = self._run(b"warning: x [/a/one.proj]\n", b"warning: x [/b/two.proj]\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["added"], [])

    def test_custom_pattern(self):
        r = self._run(b"", b"deprecated x\nwarning y\n", "--pattern", "deprecated")
        res = json.loads(r.stdout)
        self.assertEqual(res["added"], ["deprecated x"])

    def test_bad_pattern_exit_2(self):
        r = self._run(b"", b"", "--pattern", "(")
        self.assertEqual(r.returncode, 2)
        self.assertNotIn(b"Traceback", r.stderr)

    def test_missing_file_exit_2(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.dir / "x"), str(self.dir / "y")],
            capture_output=True)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn(b"Traceback", r.stderr)

    def test_odd_bytes_tolerated(self):
        r = self._run(b"", b"warning \xff\xfe bad\n")
        self.assertEqual(r.returncode, 1)

    def test_added_warning_with_nonpositive_delta_exit_1(self):
        r = self._run(b"warning: old one\nwarning: old two\n", b"warning: brand new\n")
        self.assertEqual(r.returncode, 1)
        res = json.loads(r.stdout)
        self.assertEqual(res["delta"], -1)
        self.assertEqual(res["added"], ["warning: brand new"])
        t = subprocess.run([sys.executable, str(SCRIPT), str(self.dir / "base.log"),
                            str(self.dir / "branch.log")], capture_output=True)
        self.assertEqual(t.returncode, 1)
        self.assertIn(b"+ warning: brand new", t.stdout)

    def test_removed_only_exit_0(self):
        r = self._run(b"warning: old one\n", b"")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["delta"], -1)


if __name__ == "__main__":
    unittest.main()
