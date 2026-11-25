from __future__ import annotations

import sys
import unittest

from tests.helpers import REPO_ROOT, SCRIPTS, TmpRepo

sys.path.insert(0, str(SCRIPTS))
from prlib.profile import read_profile  # noqa: E402

TEMPLATE = REPO_ROOT / "references" / "profile-template.md"
EXAMPLES = REPO_ROOT / "examples" / "profiles"


def load_example(name):
    text = (EXAMPLES / name).read_text(encoding="utf-8")
    with TmpRepo() as repo:
        repo.write(".pr-ready/profile.md", text)
        return read_profile(repo.dir)


class ProfileTemplateTest(unittest.TestCase):
    def test_profile_template_round_trips(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        with TmpRepo() as repo:
            repo.write(".pr-ready/profile.md", text)
            profile = read_profile(repo.dir)
        self.assertTrue(profile["found"])
        self.assertEqual(profile["warnings"], [])
        self.assertEqual(profile["generated"], ["src/api/generated/**", "**/*.pb.go"])
        self.assertEqual(profile["risk_paths"], [
            "**/auth*/**", "**/migrations/**", ".github/workflows/**", "openapi*"])
        self.assertEqual(profile["budget"], 500)
        self.assertEqual(profile["policy"], {
            "ai_description": "allowed", "ai_disclosure": "none",
            "prior_approval": "not-required"})

    def test_known_traps_header_present(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("| Symptom | Cause | What to do |", text)

    def test_example_node_gitlab_loads_clean(self):
        profile = load_example("node-gitlab.md")
        self.assertTrue(profile["found"])
        self.assertEqual(profile["warnings"], [])
        self.assertEqual(profile["generated"], ["src/graphql/generated/**", "**/*.snap"])
        self.assertIn(".gitlab-ci.yml", profile["risk_paths"])
        self.assertEqual(profile["policy"], {
            "ai_description": "allowed", "ai_disclosure": "required-in-trailer",
            "prior_approval": "not-required"})

    def test_example_python_no_ci_loads_clean(self):
        profile = load_example("python-no-ci.md")
        self.assertTrue(profile["found"])
        self.assertEqual(profile["warnings"], [])
        self.assertEqual(profile["generated"], [])
        self.assertEqual(profile["budget"], 300)
        self.assertEqual(profile["policy"], {
            "ai_description": "unclear", "ai_disclosure": "unclear",
            "prior_approval": "required"})

    def test_example_go_bitbucket_loads_clean(self):
        profile = load_example("go-bitbucket.md")
        self.assertTrue(profile["found"])
        self.assertEqual(profile["warnings"], [])
        self.assertEqual(profile["generated"], [
            "internal/store/sqlcdb/**", "**/*_mock.go"])
        self.assertEqual(profile["budget"], 400)
        self.assertEqual(profile["policy"], {
            "ai_description": "forbidden", "ai_disclosure": "required-in-description",
            "prior_approval": "not-required"})

    def test_examples_dir_has_exactly_the_tested_profiles(self):
        names = sorted(p.name for p in EXAMPLES.glob("*.md"))
        self.assertEqual(names, ["go-bitbucket.md", "node-gitlab.md", "python-no-ci.md"])


if __name__ == "__main__":
    unittest.main()
