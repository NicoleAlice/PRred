"""Project with no tests and no CI; the branch adds a small function."""
from __future__ import annotations

from .prove_base import NO_COMMANDS, build_repo, profile

TEXT = '''"""Text helpers."""


def title_case(text):
    return " ".join(w.capitalize() for w in text.split())
'''

TEXT_NEW = TEXT + '''

def slugify(text):
    """Lowercase, hyphen-separated slug."""
    return "-".join(text.lower().split())
'''


def build(dir):
    build_repo(
        dir,
        {"README.md": "# textkit\n\nTiny text helpers. No test suite yet.\n",
         "textkit/__init__.py": "",
         "textkit/text.py": TEXT,
         ".pr-ready/profile.md": profile(NO_COMMANDS)},
        {"textkit/text.py": TEXT_NEW},
        "Add slugify", "feat/slugify")
