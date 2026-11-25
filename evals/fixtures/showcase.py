"""Showcase: an invented webhook relay on a feature branch with four planted faults.

The branch adds delivery retries in four commits (retry policy, sender, CI,
docs). It has a committed profile and no evidence. Planted, one per cold-review
category 2-5 (`references/cold-review-prompt.md`):

2. secret:    `.gitlab-ci.yml` gives RELAY_DEPLOY_TOKEN to the `build` job,
              whose script never uses it (only `deploy` does).
3. pipeline:  the `nightly-smoke` job runs only when CI_PIPELINE_SOURCE is
              "scheduled"; GitLab sets "schedule", so it never runs.
4. premise:   `tests/test_retry.py::test_gives_up_after_max_attempts` asserts
              nothing, so "gives up after max attempts" is untested.
5. comment:   `relay/retry.py` says a 4xx is never retried; `should_retry`
              retries every status >= 400.

FAULT_LINES gives the exact lines, checked by tests/test_showcase_fixture.py.
"""
from __future__ import annotations

from .lib import make_repo

ORIGIN = "git@gitlab.example.com:team/hookrelay.git"
BRANCH = "feat/RELAY-12-delivery-retries"

GITIGNORE = ".pr-ready/evidence/\n__pycache__/\n*.pyc\ndist/\n"

README = """# hookrelay

Relays webhooks from internal services to subscriber URLs.

Run the tests with `python -m unittest discover -s tests -v`.
"""

README_NEW = README + """
## Delivery retries

A failed delivery is retried with exponential backoff: 0.5 s, 1 s, 2 s, 4 s,
then given up after five attempts. Only server errors (5xx) are retried.
"""

CONFIG = '''"""Settings read from the environment."""
import os


def subscriber_timeout():
    return float(os.environ.get("RELAY_TIMEOUT", "5"))
'''

SENDER = '''"""Deliver one webhook to one subscriber."""


def deliver(url, payload, transport):
    """Post payload to url once; return the HTTP status."""
    return transport.post(url, payload)
'''

RETRY = '''"""Retry policy for webhook deliveries."""

MAX_ATTEMPTS = 5
BASE_DELAY = 0.5


def backoff(attempt):
    """Seconds to wait before retry number `attempt` (1-based)."""
    return BASE_DELAY * (2 ** (attempt - 1))


def should_retry(status):
    # Only server errors are retried: a 4xx means the subscriber rejected the
    # payload, and sending it again cannot succeed, so it is never retried.
    return status >= 400
'''

SENDER_NEW = '''"""Deliver one webhook to one subscriber."""
import time

from relay.retry import MAX_ATTEMPTS, backoff, should_retry


class Result(object):
    def __init__(self, status, attempts):
        self.status = status
        self.attempts = attempts
        self.delivered = 200 <= status < 300


def deliver(url, payload, transport, sleep=time.sleep):
    """Post payload to url, retrying per relay.retry; return a Result."""
    attempt = 1
    while True:
        status = transport.post(url, payload)
        if not should_retry(status) or attempt >= MAX_ATTEMPTS:
            return Result(status, attempt)
        sleep(backoff(attempt))
        attempt += 1
'''

FAKE = '''class FakeTransport(object):
    """Answers each post with the next status from a list."""

    def __init__(self, statuses):
        self.statuses = list(statuses)
        self.calls = 0

    def post(self, url, payload):
        self.calls += 1
        return self.statuses.pop(0)
'''

TEST_SENDER = '''import unittest

from relay.sender import deliver
from tests.fakes import FakeTransport


class DeliverTest(unittest.TestCase):
    def test_returns_status(self):
        result = deliver("https://hooks.example.com/a", {"id": 1}, FakeTransport([200]))
        self.assertEqual(result.status, 200)
'''

TEST_RETRY = '''import unittest

from relay.retry import backoff
from relay.sender import deliver
from tests.fakes import FakeTransport


class BackoffTest(unittest.TestCase):
    def test_doubles(self):
        self.assertEqual([backoff(n) for n in (1, 2, 3, 4)], [0.5, 1.0, 2.0, 4.0])


class DeliverRetryTest(unittest.TestCase):
    def test_retries_then_succeeds(self):
        transport = FakeTransport([503, 503, 200])
        result = deliver("https://hooks.example.com/a", {"id": 1}, transport,
                         sleep=lambda s: None)
        self.assertTrue(result.delivered)
        self.assertEqual(transport.calls, 3)

    def test_gives_up_after_max_attempts(self):
        transport = FakeTransport([503] * 10)
        deliver("https://hooks.example.com/a", {"id": 1}, transport,
                sleep=lambda s: None)
'''

CI = """stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.12
  script:
    - python -m unittest discover -s tests -v

build:
  stage: build
  image: python:3.12
  script:
    - python tools/package.py
  artifacts:
    paths:
      - dist/

deploy:
  stage: deploy
  image: python:3.12
  script:
    - python tools/deploy.py
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
"""

CI_NEW = """stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.12
  script:
    - python -m unittest discover -s tests -v

build:
  stage: build
  image: python:3.12
  variables:
    RELAY_DEPLOY_TOKEN: $RELAY_DEPLOY_TOKEN
  script:
    - python tools/package.py
  artifacts:
    paths:
      - dist/

nightly-smoke:
  stage: test
  image: python:3.12
  script:
    - python -m tools.smoke
  rules:
    - if: '$CI_PIPELINE_SOURCE == "scheduled"'

deploy:
  stage: deploy
  image: python:3.12
  script:
    - python tools/deploy.py
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
"""

PACKAGE = '''"""Build dist/hookrelay.zip from the relay package."""
import os
import zipfile

os.makedirs("dist", exist_ok=True)
with zipfile.ZipFile("dist/hookrelay.zip", "w") as zf:
    for name in ("relay/__init__.py", "relay/config.py", "relay/sender.py",
                 "relay/retry.py"):
        if os.path.exists(name):
            zf.write(name)
'''

DEPLOY = '''"""Upload dist/hookrelay.zip using the deploy token from the environment."""
import os

token = os.environ.get("RELAY_DEPLOY_TOKEN")
if not token:
    raise SystemExit("RELAY_DEPLOY_TOKEN is not set")
print("would upload dist/hookrelay.zip")
'''

SMOKE = '''"""Nightly smoke check: deliver one webhook to a local fake and expect success."""
from relay.sender import deliver
from tests.fakes import FakeTransport

result = deliver("https://hooks.example.com/smoke", {"ping": True},
                 FakeTransport([503, 200]), sleep=lambda s: None)
if not result.delivered:
    raise SystemExit("smoke delivery failed")
print("smoke ok after %d attempts" % result.attempts)
'''

PROFILE = """# pr-ready profile

## Platform

- host: gitlab
- tracker: none
- stack tool: plain branches

## Project rules

- contributing: none found
- pr template: none
- commit format: free-form (observed in history)
- agent rules: none
- ai_description: allowed
  > "no statement found" (README.md)
- ai_disclosure: none
  > "no statement found" (README.md)
- prior_approval: not-required
  > "no statement found" (README.md)

## Base branch

- base: main

## Commands

- reproduce CI: `python -m unittest discover -s tests -v`
- tests: `python -m unittest discover -s tests -v`
- build: `python tools/package.py`
- generated check: none found

## Generated files

- none

## Budget

- max_lines: 500

## Risk paths

- `.gitlab-ci.yml`
- `tools/deploy.py`
"""

# Exact locations of the planted faults on the feature branch (1-based).
FAULT_LINES = {
    "secret": (".gitlab-ci.yml", 15, 16),
    "pipeline": (".gitlab-ci.yml", 29, 29),
    "premise": ("tests/test_retry.py", 21, 24),
    "comment": ("relay/retry.py", 12, 15),
}


def build(dir):
    make_repo(dir, [
        {"files": {
            ".gitignore": GITIGNORE,
            "README.md": README,
            "requirements.txt": "\n",
            "relay/__init__.py": "",
            "relay/config.py": CONFIG,
            "relay/sender.py": SENDER,
            "tests/__init__.py": "",
            "tests/fakes.py": FAKE,
            "tests/test_sender.py": TEST_SENDER.replace(
                "        result = deliver(", "        status = deliver(").replace(
                "result.status, 200", "status, 200"),
            "tools/package.py": PACKAGE,
            "tools/deploy.py": DEPLOY,
            ".gitlab-ci.yml": CI,
            ".pr-ready/profile.md": PROFILE,
        }, "commit": "Relay webhooks to subscribers"},
        {"branch": BRANCH, "files": {"relay/retry.py": RETRY},
         "commit": "Add retry policy for deliveries"},
        {"files": {"relay/sender.py": SENDER_NEW, "tests/test_sender.py": TEST_SENDER,
                   "tests/test_retry.py": TEST_RETRY},
         "commit": "Retry failed deliveries with backoff"},
        {"files": {".gitlab-ci.yml": CI_NEW, "tools/smoke.py": SMOKE},
         "commit": "CI: nightly smoke delivery"},
        {"files": {"README.md": README_NEW},
         "commit": "Document delivery retries"},
    ], remote=ORIGIN)
