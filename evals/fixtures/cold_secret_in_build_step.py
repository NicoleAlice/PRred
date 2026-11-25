"""Branch edits .gitlab-ci.yml and exposes DEPLOY_TOKEN to the build job, which does not need it."""
from __future__ import annotations

from .prove_base import TESTED_COMMANDS, build_repo, profile

CI = '''stages:
  - build
  - deploy

build:
  stage: build
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - python -m unittest discover -s tests -v
    - python tools/package.py

deploy:
  stage: deploy
  image: python:3.12
  script:
    - python tools/deploy.py
  only:
    - main
'''

CI_NEW = '''stages:
  - build
  - deploy

variables:
  DEPLOY_TOKEN: $DEPLOY_TOKEN
  PIP_CACHE_DIR: .cache/pip

build:
  stage: build
  image: python:3.12
  cache:
    paths:
      - .cache/pip
  script:
    - pip install -r requirements.txt
    - python -m unittest discover -s tests -v
    - python tools/package.py

deploy:
  stage: deploy
  image: python:3.12
  script:
    - python tools/deploy.py
  only:
    - main
'''

PACKAGE = '''"""Build the distributable archive."""
import zipfile

with zipfile.ZipFile("dist.zip", "w") as zf:
    zf.write("app/main.py")
'''

DEPLOY = '''"""Upload dist.zip using the deploy token from the environment."""
import os

token = os.environ.get("DEPLOY_TOKEN")
if not token:
    raise SystemExit("DEPLOY_TOKEN is not set")
print("would upload dist.zip")
'''

TEST = '''import unittest

from app.main import greet


class GreetTest(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Ana"), "Hello, Ana")


if __name__ == "__main__":
    unittest.main()
'''


def build(dir):
    build_repo(
        dir,
        {"README.md": "# app\n\nTiny app. Tests: `python -m unittest discover -s tests`.\n",
         "requirements.txt": "\n",
         "app/__init__.py": "",
         "app/main.py": 'def greet(name):\n    return "Hello, " + name\n',
         "tools/package.py": PACKAGE,
         "tools/deploy.py": DEPLOY,
         "tests/__init__.py": "",
         "tests/test_main.py": TEST,
         ".gitlab-ci.yml": CI,
         ".pr-ready/profile.md": profile(TESTED_COMMANDS).replace(
             "- host: github", "- host: gitlab")},
        {".gitlab-ci.yml": CI_NEW},
        "Cache pip downloads in CI", "feat/ci-pip-cache")
