from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "compare_generated.py"


class CompareGeneratedTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def _run(self, a, b, *extra):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(a), str(b)] + list(extra),
            capture_output=True)

    def _file(self, name, data):
        p = self.dir / name
        p.write_bytes(data)
        return p

    def test_crlf_only_is_equal(self):
        a = self._file("a", b"one\r\ntwo\r\n")
        b = self._file("b", b"one\ntwo\n")
        r = self._run(a, b, "--json")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout), {"equal": True, "first_diff_line": None})

    def test_content_difference_reports_line_3(self):
        a = self._file("a", b"one\r\ntwo\r\nthree\r\n")
        b = self._file("b", b"one\ntwo\nTHREE\n")
        r = self._run(a, b, "--json")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stdout), {"equal": False, "first_diff_line": 3})

    def test_prefix_reports_line_past_shorter(self):
        a = self._file("a", b"one\ntwo\n")
        b = self._file("b", b"one\ntwo\nthree\n")
        r = self._run(a, b, "--json")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stdout)["first_diff_line"], 3)

    def test_missing_trailing_newline_differs_past_shorter(self):
        a = self._file("a", b"x")
        b = self._file("b", b"x\n")
        r = self._run(a, b, "--json")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stdout)["first_diff_line"], 2)

    def test_human_output(self):
        a = self._file("a", b"x\n")
        b = self._file("b", b"y\n")
        r = self._run(a, b)
        self.assertEqual(r.returncode, 1)
        self.assertIn(b"line 1", r.stdout)

    def test_missing_file_exit_2(self):
        a = self._file("a", b"x\n")
        r = self._run(a, self.dir / "nope")
        self.assertEqual(r.returncode, 2)
        self.assertNotIn(b"Traceback", r.stderr)
        self.assertTrue(r.stderr.strip())


if __name__ == "__main__":
    unittest.main()
