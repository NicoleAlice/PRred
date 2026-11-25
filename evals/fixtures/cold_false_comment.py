"""Branch adds read_report; a comment claims `name` is validated upstream, nothing does."""
from __future__ import annotations

from .prove_base import TESTED_COMMANDS, build_repo, profile

STORE = '''"""Report storage helpers."""
import os

REPORT_DIR = "reports"


def list_reports(base=REPORT_DIR):
    return sorted(os.listdir(base))
'''

STORE_NEW = STORE + '''

# name is validated upstream by the API layer, so it is safe to use as a path.
def read_report(name, base=REPORT_DIR):
    path = os.path.join(base, name + ".txt")
    with open(path, encoding="utf-8") as fh:
        return fh.read()
'''

BASE_TEST = '''import os
import tempfile
import unittest

from reports.store import list_reports


class ListReportsTest(unittest.TestCase):
    def test_lists_sorted(self):
        with tempfile.TemporaryDirectory() as tmp:
            for n in ("b.txt", "a.txt"):
                open(os.path.join(tmp, n), "w").close()
            self.assertEqual(list_reports(tmp), ["a.txt", "b.txt"])


if __name__ == "__main__":
    unittest.main()
'''

NEW_TEST = '''import os
import tempfile
import unittest

from reports.store import read_report


class ReadReportTest(unittest.TestCase):
    def test_reads_existing_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "q1.txt"), "w", encoding="utf-8") as fh:
                fh.write("revenue up")
            self.assertEqual(read_report("q1", tmp), "revenue up")

    def test_missing_report_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                read_report("nope", tmp)


if __name__ == "__main__":
    unittest.main()
'''


def build(dir):
    build_repo(
        dir,
        {"README.md": "# reports\n\nTiny report store. Tests: `python -m unittest discover -s tests`.\n",
         "reports/__init__.py": "",
         "reports/store.py": STORE,
         "tests/__init__.py": "",
         "tests/test_list.py": BASE_TEST,
         ".pr-ready/profile.md": profile(TESTED_COMMANDS)},
        {"reports/store.py": STORE_NEW,
         "tests/test_read.py": NEW_TEST},
        "Add read_report", "feat/read-report")
