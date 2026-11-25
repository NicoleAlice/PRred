"""Project with no remote, no CI and no contribution docs."""
from __future__ import annotations

from .lib import make_repo


def build(dir):
    make_repo(dir, [
        {"files": {
            "README.md": "# notes\n\nA small note-taking helper.\n",
            "notes/__init__.py": "",
            "notes/store.py": (
                "def add(items, text):\n"
                "    return items + [text]\n"
            ),
        }, "commit": "Add note store"},
    ])
