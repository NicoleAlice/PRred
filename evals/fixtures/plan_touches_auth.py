"""Small service with src/auth/ (login and token check)."""
from __future__ import annotations

from .lib import make_repo

FILES = {
    "README.md": "# demo-portal\n\nInternal portal API. Tests: `python -m unittest discover -s tests`.\n",
    "src/__init__.py": "",
    "src/auth/__init__.py": "",
    "src/auth/login.py": '''"""Password login that returns a short-lived access token."""
from __future__ import annotations

from src.auth import tokens

USERS = {"ana@example.com": "correct horse"}


def login(email, password):
    if USERS.get(email) != password:
        raise PermissionError("bad credentials")
    return tokens.issue(email, ttl_seconds=900)
''',
    "src/auth/tokens.py": '''"""Issue and check signed tokens."""
from __future__ import annotations

import hashlib
import hmac
import time

SECRET = b"dev-only-secret"


def _sign(payload):
    return hmac.new(SECRET, payload.encode(), hashlib.sha256).hexdigest()


def issue(subject, ttl_seconds, now=None):
    expires = int((now if now is not None else time.time()) + ttl_seconds)
    payload = "%s|%d" % (subject, expires)
    return payload + "|" + _sign(payload)


def check(token, now=None):
    """Return the subject if the token is valid and not expired, else None."""
    try:
        subject, expires, signature = token.rsplit("|", 2)
    except ValueError:
        return None
    if not hmac.compare_digest(signature, _sign("%s|%s" % (subject, expires))):
        return None
    if int(expires) < (now if now is not None else time.time()):
        return None
    return subject
''',
    "src/api/__init__.py": "",
    "src/api/profile.py": '''"""Profile endpoint guarded by the token check."""
from __future__ import annotations

from src.auth import tokens


def get_profile(token):
    subject = tokens.check(token)
    if subject is None:
        raise PermissionError("invalid token")
    return {"email": subject}
''',
    "tests/__init__.py": "",
    "tests/test_tokens.py": '''import unittest

from src.auth import tokens


class TokensTest(unittest.TestCase):
    def test_roundtrip(self):
        t = tokens.issue("ana@example.com", 60, now=1000)
        self.assertEqual(tokens.check(t, now=1010), "ana@example.com")

    def test_expired(self):
        t = tokens.issue("ana@example.com", 60, now=1000)
        self.assertIsNone(tokens.check(t, now=2000))


if __name__ == "__main__":
    unittest.main()
''',
}


def build(dir):
    make_repo(dir, [{"files": FILES, "commit": "Add login and token check"}])
