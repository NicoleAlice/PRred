from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import REPO_ROOT, SCRIPTS, run_git

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(SCRIPTS))
from evals.fixtures import showcase  # noqa: E402
from prlib.profile import read_profile  # noqa: E402

CASES = REPO_ROOT / "evals" / "showcase" / "cases.json"

# What each planted fault's lines must contain.
FAULT_TEXT = {
    "secret": "RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN",
    "pipeline": "$CI_PIPELINE_SOURCE == \"scheduled\"",
    "premise": "def test_gives_up_after_max_attempts",
    "comment": "never retried",
}


class ShowcaseFixtureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = os.path.realpath(tempfile.mkdtemp(prefix="showcase-"))
        cls.dir = os.path.join(cls.tmp, "repo")
        showcase.build(cls.dir)

    @classmethod
    def tearDownClass(cls):
        def onerror(func, path, _info):
            os.chmod(path, 0o700)
            func(path)
        shutil.rmtree(cls.tmp, onerror=onerror)

    def lines(self, rel):
        return Path(self.dir, rel).read_text(encoding="utf-8").splitlines()

    def test_branch_has_four_commits_on_main(self):
        self.assertEqual(run_git(["branch", "--show-current"], self.dir), showcase.BRANCH)
        log = run_git(["log", "--oneline", "main..HEAD"], self.dir).splitlines()
        self.assertEqual(len(log), 4)
        self.assertEqual(run_git(["status", "--porcelain"], self.dir), "")

    def test_profile_valid_and_no_evidence(self):
        profile = read_profile(self.dir)
        self.assertTrue(profile["found"])
        self.assertEqual(profile["warnings"], [])
        self.assertFalse(Path(self.dir, ".pr-ready", "evidence").exists())

    def test_fault_lines_hold_the_planted_faults(self):
        for key, (rel, start, end) in showcase.FAULT_LINES.items():
            chunk = "\n".join(self.lines(rel)[start - 1:end])
            self.assertIn(FAULT_TEXT[key], chunk, key)

    def test_comment_contradicts_code(self):
        rel, start, end = showcase.FAULT_LINES["comment"]
        chunk = "\n".join(self.lines(rel)[start - 1:end])
        self.assertIn("return status >= 400", chunk)

    def test_assertionless_test_has_no_assert(self):
        rel, start, end = showcase.FAULT_LINES["premise"]
        body = "\n".join(self.lines(rel)[start - 1:end])
        self.assertNotIn("assert", body)
        self.assertEqual(len(self.lines(rel)), end, "the test must be the last in the file")

    def test_build_job_does_not_use_the_token(self):
        ci = Path(self.dir, ".gitlab-ci.yml").read_text(encoding="utf-8")
        self.assertNotIn("RELAY_DEPLOY_TOKEN", Path(self.dir, "tools/package.py").read_text("utf-8"))
        self.assertIn("RELAY_DEPLOY_TOKEN", Path(self.dir, "tools/deploy.py").read_text("utf-8"))
        self.assertEqual(ci.count("RELAY_DEPLOY_TOKEN"), 2)

    def test_suite_and_smoke_pass(self):
        for args in (["-m", "unittest", "discover", "-s", "tests"], ["-m", "tools.smoke"]):
            r = subprocess.run([sys.executable, "-B"] + args, cwd=self.dir,
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_rubric_cites_the_fault_lines(self):
        case = json.loads(CASES.read_text(encoding="utf-8"))["cases"][0]
        rubric = case["rubric"]
        self.assertEqual(len(rubric), 5)
        for item, key in zip(rubric, ("secret", "pipeline", "comment", "premise")):
            rel, start, end = showcase.FAULT_LINES[key]
            self.assertIn("`%s`" % rel, item, key)
            nums = [int(n) for n in re.findall(r"\bline[s]? (?:from )?(\d+)", item)]
            self.assertTrue(nums and start <= nums[0] <= end, (key, item))
        self.assertTrue(case["prompt"].startswith("Get this branch ready for review."))
        self.assertIn("No commits and no remote actions", rubric[4])

    def test_with_prompt_points_at_pr_ready(self):
        out = os.path.join(self.tmp, "with run")
        r = subprocess.run(
            [sys.executable, str(REPO_ROOT / "evals" / "setup.py"), "showcase",
             "end-to-end", "with", out],
            capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("/.claude/skills/pr-ready/SKILL.md", r.stdout)
        self.assertTrue(Path(out, ".claude", "skills", "pr-ready", "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
