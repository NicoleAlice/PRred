"""Branch adds a correct, well-tested helper with accurate comments."""
from __future__ import annotations

from .prove_base import TESTED_COMMANDS, build_repo, profile

TEXT = '''"""Text helpers."""


def title_case(s):
    return s.title()
'''

TEXT_NEW = TEXT + '''

def truncate(s, limit):
    """Return s cut to at most `limit` characters, ending in "..." when cut."""
    if limit < 3:
        raise ValueError("limit must be at least 3")
    if len(s) <= limit:
        return s
    # Reserve three characters for the ellipsis so the result fits `limit`.
    return s[: limit - 3] + "..."
'''

BASE_TEST = '''import unittest

from textkit.text import title_case


class TitleCaseTest(unittest.TestCase):
    def test_title_case(self):
        self.assertEqual(title_case("hello world"), "Hello World")


if __name__ == "__main__":
    unittest.main()
'''

NEW_TEST = '''import unittest

from textkit.text import truncate


class TruncateTest(unittest.TestCase):
    def test_short_string_unchanged(self):
        self.assertEqual(truncate("abc", 5), "abc")

    def test_exact_length_unchanged(self):
        self.assertEqual(truncate("abcde", 5), "abcde")

    def test_long_string_cut_with_ellipsis(self):
        self.assertEqual(truncate("abcdefgh", 6), "abc...")

    def test_result_never_exceeds_limit(self):
        self.assertLessEqual(len(truncate("x" * 50, 10)), 10)

    def test_limit_below_three_rejected(self):
        with self.assertRaises(ValueError):
            truncate("abcdef", 2)


if __name__ == "__main__":
    unittest.main()
'''


def build(dir):
    build_repo(
        dir,
        {"README.md": "# textkit\n\nTiny text helpers. Tests: `python -m unittest discover -s tests`.\n",
         "textkit/__init__.py": "",
         "textkit/text.py": TEXT,
         "tests/__init__.py": "",
         "tests/test_title.py": BASE_TEST,
         ".pr-ready/profile.md": profile(TESTED_COMMANDS)},
        {"textkit/text.py": TEXT_NEW,
         "tests/test_truncate.py": NEW_TEST},
        "Add truncate", "feat/truncate")
