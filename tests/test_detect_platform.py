from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import detect_platform as dp  # noqa: E402
from detect_platform import detect_platform  # noqa: E402
from tests.helpers import TmpRepo  # noqa: E402


def _repo(test, remote=None):
    repo = TmpRepo()
    test.addCleanup(repo.cleanup)
    repo.write("README.md", "hi\n")
    repo.commit("init")
    if remote:
        repo.git("remote", "add", "origin", remote)
    return repo


class DetectPlatformTest(unittest.TestCase):
    def test_no_remote_host_none(self):
        res = detect_platform(_repo(self).dir)
        self.assertEqual(res["host"], "none")
        self.assertIsNone(res["remote_url"])

    def test_gitlab_remote(self):
        res = detect_platform(_repo(self, "git@gitlab.example.com:a/b.git").dir)
        self.assertEqual(res["host"], "gitlab")
        self.assertEqual(res["remote_url"], "git@gitlab.example.com:a/b.git")

    def test_gitlab_https_and_github_variants(self):
        cases = [
            ("https://gitlab.example.com/a/b.git", "gitlab"),
            ("https://github.com/a/b.git", "github"),
            ("git@github.com:a/b.git", "github"),
            ("git@bitbucket.org:a/b.git", "bitbucket"),
            ("https://github.com/org/gitlab-tools.git", "github"),
            ("https://gitlab.com/o/github.com-x.git", "gitlab"),
            ("https://dev.azure.com/org/p/_git/r", "azure-devops"),
            ("https://org.visualstudio.com/p/_git/r", "azure-devops"),
        ]
        for url, host in cases:
            self.assertEqual(detect_platform(_repo(self, url).dir)["host"], host, url)

    def test_self_hosted_unknown(self):
        res = detect_platform(_repo(self, "https://git.example.org/a/b.git").dir)
        self.assertEqual(res["host"], "unknown")
        res = detect_platform(_repo(self, "https://git.example.org/gitlab-x/r.git").dir)
        self.assertEqual(res["host"], "unknown")

    def test_password_with_at_sign_fully_stripped(self):
        res = detect_platform(_repo(self, "https://user:p@ss@github.com/a/b").dir)
        self.assertEqual(res["remote_url"], "https://github.com/a/b")
        self.assertEqual(res["host"], "github")

    def test_credentials_stripped(self):
        res = detect_platform(
            _repo(self, "https://user:s3cret@github.com/a/b.git").dir)
        self.assertEqual(res["host"], "github")
        self.assertNotIn("s3cret", json.dumps(res))
        self.assertEqual(res["remote_url"], "https://github.com/a/b.git")
        res = detect_platform(_repo(self, "https://tok3n@gitlab.example.com/a/b.git").dir)
        self.assertNotIn("tok3n", json.dumps(res))

    def test_finds_contributing_mr_template_and_gitlab_ci(self):
        repo = _repo(self)
        repo.write("CONTRIBUTING.md", "c\n")
        repo.write("docs/contributing.md", "c\n")
        repo.write("AI_POLICY.md", "p\n")
        repo.write(".gitlab/merge_request_templates/Default.md", "t\n")
        repo.write(".github/workflows/ci.yml", "x\n")
        repo.write(".gitlab-ci.yml", "x\n")
        repo.write("CLAUDE.md", "r\n")
        repo.write(".cursor/rules/a.mdc", "r\n")
        repo.write("untracked-dir/ignored.txt", "z\n")
        repo.git("add", "-A")
        repo.git("commit", "-m", "files")
        repo.write("CONTRIBUTING-extra.md", "untracked\n")
        res = detect_platform(repo.dir)
        self.assertEqual(res["policy_files"],
                         ["AI_POLICY.md", "CONTRIBUTING.md", "docs/contributing.md"])
        self.assertEqual(res["pr_templates"],
                         [".gitlab/merge_request_templates/Default.md"])
        self.assertEqual(res["ci_files"], [".github/workflows/ci.yml", ".gitlab-ci.yml"])
        self.assertEqual(res["agent_rules"], [".cursor/rules/a.mdc", "CLAUDE.md"])

    def test_extracts_ticket_keys(self):
        repo = _repo(self)
        repo.write("a.txt", "1\n")
        repo.commit("ABC-123 add thing")
        repo.write("a.txt", "2\n")
        repo.commit("fix PROJ-9 and ABC-123 again")
        repo.git("branch", "feature/XY2-77-work")
        res = detect_platform(repo.dir)
        self.assertEqual(res["ticket_keys"], ["PROJ-9", "ABC-123", "XY2-77"])
        self.assertEqual(res["commit_samples"][0], "fix PROJ-9 and ABC-123 again")

    def test_ticket_keys_stoplist(self):
        repo = _repo(self)
        repo.write("a.txt", "1\n")
        repo.commit("use UTF-8, UTF-16, SHA-1, SHA-256, ISO-8601 dates and X-509 certs")
        repo.write("a.txt", "2\n")
        repo.commit("ABC-12 swap MD-5 for SHA-512")
        res = detect_platform(repo.dir)
        self.assertEqual(res["ticket_keys"], ["ABC-12"])

    def test_ticket_keys_capped_and_samples_20(self):
        repo = _repo(self)
        for i in range(25):
            repo.write("a.txt", "%d\n" % i)
            repo.commit("KEY-%d work" % i)
        res = detect_platform(repo.dir)
        self.assertEqual(len(res["commit_samples"]), 20)
        self.assertEqual(len(res["ticket_keys"]), 10)

    def test_empty_repo(self):
        repo = TmpRepo()
        self.addCleanup(repo.cleanup)
        res = detect_platform(repo.dir)
        self.assertEqual(res["commit_samples"], [])
        self.assertIsNone(res["default_base"])
        self.assertEqual(res["host"], "none")

    def test_default_base(self):
        self.assertEqual(detect_platform(_repo(self).dir)["default_base"], "main")

    def test_absent_clis_false(self):
        repo = _repo(self)
        with mock.patch("shutil.which", return_value=None):
            res = detect_platform(repo.dir)
        self.assertEqual(res["clis"], {"gh": False, "glab": False, "az": False, "bb": False})
        self.assertEqual(res["stack_tools"],
                         {"gh_stack": False, "graphite": False, "sapling": False})

    def test_probe_results_used(self):
        repo = _repo(self)
        with mock.patch.object(dp, "_probe", lambda cmd, args: cmd == "gh" and args == ["--version"]):
            res = detect_platform(repo.dir)
        self.assertTrue(res["clis"]["gh"])
        self.assertFalse(res["clis"]["glab"])
        self.assertFalse(res["stack_tools"]["gh_stack"])

    def test_probe_timeout_false(self):
        import subprocess
        with mock.patch("shutil.which", return_value="/x/gh"), \
                mock.patch("subprocess.run",
                           side_effect=subprocess.TimeoutExpired("gh", 5)):
            self.assertFalse(dp._probe("gh", ["--version"]))
        with mock.patch("shutil.which", return_value="/x/gh"), \
                mock.patch("subprocess.run", side_effect=OSError("boom")):
            self.assertFalse(dp._probe("gh", ["--version"]))

    def test_cli_json_and_not_a_repo(self):
        repo = _repo(self, "git@github.com:a/b.git")
        r = repo.run("detect_platform.py", "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["host"], "github")
        r = repo.run("detect_platform.py")
        self.assertEqual(r.returncode, 0)
        self.assertIn("github", r.stdout)
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            import subprocess
            p = subprocess.run([sys.executable, str(Path(dp.__file__)), "--json"],
                               cwd=d, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(p.returncode, 2)
            self.assertNotIn("Traceback", p.stderr)


if __name__ == "__main__":
    unittest.main()
