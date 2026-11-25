from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from prlib.git import GitError, current_branch, head_sha, merge_base, resolve_base  # noqa: E402
from prlib.globs import glob_to_regex, matches_any  # noqa: E402
from prlib.profile import read_profile  # noqa: E402
from tests.helpers import TmpRepo, run_git  # noqa: E402


class ResolveBaseTests(unittest.TestCase):
    def test_resolve_base_prefers_origin_head(self):
        with TmpRepo() as src, tempfile.TemporaryDirectory() as tmp:
            src.write("a.txt", "a\n")
            src.commit("init")
            src.git("branch", "-m", "trunk")
            bare = str(Path(tmp) / "bare.git")
            run_git(["clone", "--bare", src.dir, bare], tmp)
            run_git(["symbolic-ref", "HEAD", "refs/heads/trunk"], bare)
            clone = str(Path(tmp) / "clone")
            run_git(["clone", bare, clone], tmp)
            run_git(["checkout", "-b", "feature"], clone)
            self.assertEqual(resolve_base(clone), "origin/trunk")

    def test_resolve_base_explicit(self):
        with TmpRepo() as r:
            r.write("a.txt", "a\n")
            r.commit("init")
            r.git("branch", "dev")
            self.assertEqual(resolve_base(r.dir, "dev"), "dev")

    def test_resolve_base_falls_back_main_then_master(self):
        with TmpRepo() as r:
            r.write("a.txt", "a\n")
            r.commit("init")
            self.assertEqual(resolve_base(r.dir), "main")
            r.git("branch", "-m", "master")
            self.assertEqual(resolve_base(r.dir), "master")

    def test_resolve_base_errors_clearly(self):
        with TmpRepo() as r:
            r.write("a.txt", "a\n")
            r.commit("init")
            r.git("branch", "-m", "dev")
            with self.assertRaisesRegex(GitError, "cannot resolve base; pass --base"):
                resolve_base(r.dir)

    def test_current_branch_detached(self):
        with TmpRepo() as r:
            r.write("a.txt", "a\n")
            sha = r.commit("init")
            self.assertEqual(current_branch(r.dir), "main")
            r.git("checkout", "--detach")
            self.assertEqual(current_branch(r.dir), "detached")
            self.assertEqual(head_sha(r.dir), sha)

    def test_merge_base(self):
        with TmpRepo() as r:
            r.write("a.txt", "a\n")
            base = r.commit("init")
            r.git("checkout", "-b", "feat")
            r.write("b.txt", "b\n")
            r.commit("more")
            self.assertEqual(merge_base(r.dir, "main"), base)


class GlobTests(unittest.TestCase):
    def test_glob(self):
        self.assertTrue(glob_to_regex("**/auth*/**").match("src/auth/x.ts"))
        self.assertTrue(glob_to_regex("**/auth*/**").match("authz/y.go"))
        self.assertTrue(glob_to_regex("*.md").match("a.md"))
        self.assertFalse(glob_to_regex("*.md").match("d/a.md"))
        self.assertTrue(glob_to_regex("docs/**").match("docs/a/b.md"))
        self.assertTrue(glob_to_regex("a?c").match("abc"))
        self.assertFalse(glob_to_regex("a?c").match("a/c"))
        self.assertFalse(glob_to_regex("*.md").match("A.MD"))
        self.assertTrue(glob_to_regex("*.md", ignore_case=True).match("A.MD"))

    def test_matches_any(self):
        self.assertTrue(matches_any("x/y.lock", ["*.md", "**/*.lock"]))
        self.assertFalse(matches_any("x/y.txt", ["*.md", "**/*.lock"]))
        self.assertFalse(matches_any("x", []))


SAMPLE = """# Profile

## Generated files
- `api/openapi.json`

## Risk paths
- `**/auth*/**`
- `db/migrations/**`

## Budget
max_lines: 300

## Project rules
- ai_description: forbidden — "no AI-written descriptions"
- ai_disclosure: required-in-trailer
- prior_approval: required
"""


class ProfileTests(unittest.TestCase):
    def test_read_profile_defaults_when_missing(self):
        with TmpRepo() as r:
            p = read_profile(r.dir)
            self.assertFalse(p["found"])
            self.assertEqual(p["budget"], 500)
            self.assertEqual(p["generated"], [])
            self.assertEqual(p["risk_paths"], [])
            self.assertEqual(set(p["policy"].values()), {"unclear"})

    def test_read_profile_parses_sections(self):
        with TmpRepo() as r:
            r.write(".pr-ready/profile.md", SAMPLE)
            p = read_profile(r.dir)
            self.assertTrue(p["found"])
            self.assertEqual(p["generated"], ["api/openapi.json"])
            self.assertEqual(p["risk_paths"], ["**/auth*/**", "db/migrations/**"])
            self.assertEqual(p["budget"], 300)
            self.assertEqual(p["policy"]["ai_description"], "forbidden")
            self.assertEqual(p["policy"]["ai_disclosure"], "required-in-trailer")
            self.assertEqual(p["policy"]["prior_approval"], "required")
            self.assertEqual(p["warnings"], [])

    def test_read_profile_tolerates_junk(self):
        with TmpRepo() as r:
            r.write(".pr-ready/profile.md",
                    "## Budget\nmax_lines: lots\n\n## Project rules\n- ai_description: maybe\n")
            p = read_profile(r.dir)
            self.assertEqual(p["budget"], 500)
            self.assertEqual(p["policy"]["ai_description"], "unclear")
            self.assertEqual(len(p["warnings"]), 2)

    def test_read_profile_crlf(self):
        with TmpRepo() as r:
            r.write(".pr-ready/profile.md", SAMPLE.replace("\n", "\r\n"))
            p = read_profile(r.dir)
            self.assertEqual(p["generated"], ["api/openapi.json"])
            self.assertEqual(p["budget"], 300)


if __name__ == "__main__":
    unittest.main()
