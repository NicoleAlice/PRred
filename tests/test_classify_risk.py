from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from classify_risk import DEFAULT_RISK_PATHS, classify_risk  # noqa: E402
from tests.helpers import TmpRepo  # noqa: E402


def _repo(test, files, profile=None):
    repo = TmpRepo()
    test.addCleanup(repo.cleanup)
    if profile:
        repo.write(".pr-ready/profile.md", profile)
    repo.write("README.md", "hi\n")
    repo.commit("init")
    repo.git("checkout", "-b", "feature")
    for path, content in files.items():
        repo.write(path, content)
    repo.commit("work")
    return repo


class ClassifyRiskTest(unittest.TestCase):
    def test_docs_only_trivial(self):
        repo = _repo(self, {"docs/guide.md": "x\n", "NOTES.txt": "y\n",
                            "LICENSE": "mit\n", "img/logo.png": b"\x89PNG"})
        res = classify_risk(repo.dir)
        self.assertEqual(res["level"], "trivial")
        self.assertTrue(res["small"])
        self.assertEqual(res["reasons"], [])

    def test_src_change_normal_small(self):
        repo = _repo(self, {"src/app.py": "print(1)\n"})
        res = classify_risk(repo.dir)
        self.assertEqual(res["level"], "normal")
        self.assertTrue(res["small"])

    def test_not_small_when_over_ten(self):
        repo = _repo(self, {"src/app.py": "x\n" * 11})
        self.assertFalse(classify_risk(repo.dir)["small"])

    def test_auth_path_risky_with_reason(self):
        repo = _repo(self, {"src/auth/login.ts": "a\n", "src/ok.ts": "b\n"})
        res = classify_risk(repo.dir)
        self.assertEqual(res["level"], "risky")
        self.assertEqual(res["reasons"],
                         [{"path": "src/auth/login.ts", "rule": "risk-path:**/auth*/**"}])

    def test_profile_risk_path_adds_to_defaults(self):
        repo = _repo(self, {"billing/charge.py": "a\n", "db/migrations/001.py": "b\n"},
                     profile="## Risk paths\n- `billing/**`\n")
        res = classify_risk(repo.dir)
        self.assertEqual(res["level"], "risky")
        rules = dict((r["path"], r["rule"]) for r in res["reasons"])
        self.assertEqual(rules["billing/charge.py"], "risk-path:billing/**")
        self.assertEqual(rules["db/migrations/001.py"], "risk-path:**/migrations/**")

    def test_lockfile_counts_for_risk(self):
        repo = _repo(self, {"schema.sql": "a\n"})
        self.assertEqual(classify_risk(repo.dir)["level"], "risky")

    def test_generated_code_file_not_trivial(self):
        repo = _repo(self, {"docs/a.md": "x\n", "yarn.lock": "1\n"})
        self.assertEqual(classify_risk(repo.dir)["level"], "normal")

    def test_profile_warnings_included(self):
        repo = _repo(self, {"a.md": "x\n"},
                     profile="## Budget\nmax_lines: lots\n")
        self.assertTrue(classify_risk(repo.dir)["warnings"])

    def test_defaults_constant(self):
        self.assertIn("**/Dockerfile", DEFAULT_RISK_PATHS)
        self.assertEqual(len(DEFAULT_RISK_PATHS), 13)

    def test_cli_json(self):
        repo = _repo(self, {"src/auth/x.py": "a\n"})
        res = repo.run("classify_risk.py", "--json")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(json.loads(res.stdout)["level"], "risky")

    def test_cli_human(self):
        repo = _repo(self, {"a.md": "x\n"})
        res = repo.run("classify_risk.py")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("trivial", res.stdout)

    def test_no_base_exit_2(self):
        repo = TmpRepo()
        self.addCleanup(repo.cleanup)
        repo.write("a.txt", "x\n")
        repo.git("checkout", "-b", "feature")
        repo.commit("init")
        res = repo.run("classify_risk.py")
        self.assertEqual(res.returncode, 2)
        self.assertIn("cannot resolve base", res.stderr)
        self.assertNotIn("Traceback", res.stderr)


if __name__ == "__main__":
    unittest.main()
