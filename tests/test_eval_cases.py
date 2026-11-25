import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"


def case_files():
    return sorted(EVALS.glob("*/cases.json"))


class EvalCasesTest(unittest.TestCase):
    def test_there_are_case_files(self):
        self.assertTrue(case_files())

    def test_schema(self):
        for path in case_files():
            data = json.loads(path.read_text(encoding="utf-8"))
            ids = [c["id"] for c in data["cases"]]
            self.assertEqual(len(ids), len(set(ids)), path)
            for case in data["cases"]:
                label = "%s:%s" % (path.parent.name, case["id"])
                fixture = EVALS / "fixtures" / (case["fixture"] + ".py")
                self.assertTrue(fixture.is_file(), label)
                self.assertEqual(case["runs"], 3, label)
                self.assertTrue(case["prompt"].strip(), label)
                self.assertTrue(case["rubric"], label)
                for item in case["rubric"]:
                    self.assertTrue(item.strip(), label)
            for key in ("should", "should_not"):
                self.assertTrue(data["triggers"].get(key), "%s %s" % (path, key))

    def test_every_fixture_builds(self):
        for path in case_files():
            skill = path.parent.name
            for case in json.loads(path.read_text(encoding="utf-8"))["cases"]:
                label = "%s:%s" % (skill, case["id"])
                with tempfile.TemporaryDirectory() as tmp:
                    out = os.path.join(tmp, "out")
                    r = subprocess.run(
                        [sys.executable, str(EVALS / "setup.py"), skill,
                         case["id"], "without", out],
                        capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(r.returncode, 0, "%s %s" % (label, r.stderr))
                    self.assertTrue(os.path.isdir(os.path.join(out, ".git")), label)
                    self.assertIn(case["prompt"], r.stdout, label)


if __name__ == "__main__":
    unittest.main()
