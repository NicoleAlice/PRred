#!/usr/bin/env python3
"""Detect the git host, available CLIs, contribution policy and CI files of a repo."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prlib.git import GitError, git, resolve_base  # noqa: E402
from prlib.globs import matches_any  # noqa: E402

POLICY = ["CONTRIBUTING*", "AI_POLICY*", "AI*.md", "**/CONTRIBUTING*"]
TEMPLATES = [
    ".github/pull_request_template.md", ".github/PULL_REQUEST_TEMPLATE/**",
    "PULL_REQUEST_TEMPLATE.md", "docs/pull_request_template.md",
    ".gitlab/merge_request_templates/**", ".azuredevops/pull_request_template*",
    ".bitbucket/**pull*request*",
]
CI = [
    ".github/workflows/**", ".gitlab-ci.yml", "azure-pipelines.yml",
    "bitbucket-pipelines.yml", "Jenkinsfile", ".circleci/config.yml",
]
AGENT_RULES = ["CLAUDE.md", "AGENTS.md", ".claude/rules/**", ".cursor/rules/**"]
TICKET_RE = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")
# Look like ticket keys but name encodings, hashes and standards (UTF-8, SHA-256, ...).
TICKET_STOP_PREFIXES = {
    "UTF", "UCS", "SHA", "MD", "ISO", "RFC", "CVE", "CWE", "IEEE", "ECMA", "CRC", "PEP",
}
PROBE_TIMEOUT = 5


def _probe(cmd, args):
    """True when `cmd` is on PATH and `cmd *args` exits 0 within the timeout."""
    exe = shutil.which(cmd)
    if not exe:
        return False
    try:
        result = subprocess.run(
            [exe] + list(args), stdin=subprocess.DEVNULL, capture_output=True,
            timeout=PROBE_TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def _sanitize_url(url):
    """Drop credentials embedded in a remote URL."""
    m = re.match(r"^([A-Za-z][A-Za-z0-9+.-]*://)([^/]*)@(.*)$", url)
    if not m:
        return url
    scheme, userinfo, rest = m.groups()
    if scheme.lower().startswith("http") or ":" in userinfo:
        return scheme + rest
    return url


def _hostname(url):
    if "://" in url:
        try:
            return (urlsplit(url).hostname or "").lower()
        except ValueError:
            return ""
    # scp-style: [user@]host:path
    return url.rsplit("@", 1)[-1].split(":", 1)[0].lower()


def _host_of(url):
    name = _hostname(url)
    if "github.com" in name:
        return "github"
    if "gitlab" in name:
        return "gitlab"
    if "bitbucket.org" in name:
        return "bitbucket"
    if "dev.azure.com" in name or "visualstudio.com" in name:
        return "azure-devops"
    return "unknown"


def _tracked_files(cwd):
    out = git(["ls-files", "-z"], cwd)
    return [p for p in out.split("\0") if p]


def _select(files, globs):
    return sorted(f for f in files if matches_any(f, globs, ignore_case=True))


def detect_platform(cwd):
    git(["rev-parse", "--git-dir"], cwd)  # raises GitError outside a repo
    try:
        remote = _sanitize_url(git(["remote", "get-url", "origin"], cwd))
    except GitError:
        remote = ""
    host = _host_of(remote) if remote else "none"

    try:
        default_base = resolve_base(cwd)
    except GitError:
        default_base = None

    files = _tracked_files(cwd)

    try:
        samples = git(["log", "-20", "--format=%s"], cwd).splitlines()
    except GitError:  # no commits yet
        samples = []
    try:
        branches = git(["for-each-ref", "--format=%(refname:short)", "refs/heads"],
                       cwd).splitlines()
    except GitError:
        branches = []
    keys = []
    for text in samples + branches:
        for key in TICKET_RE.findall(text):
            if key.split("-", 1)[0] in TICKET_STOP_PREFIXES:
                continue
            if key not in keys:
                keys.append(key)

    return {
        "host": host,
        "remote_url": remote or None,
        "default_base": default_base,
        "clis": {
            "gh": _probe("gh", ["--version"]),
            "glab": _probe("glab", ["--version"]),
            "az": _probe("az", ["--version"]),
            "bb": _probe("bb", ["--version"]),
        },
        "stack_tools": {
            "gh_stack": _probe("gh", ["stack", "--help"]),
            "graphite": _probe("gt", ["--version"]),
            "sapling": _probe("sl", ["--version"]),
        },
        "policy_files": _select(files, POLICY),
        "pr_templates": _select(files, TEMPLATES),
        "ci_files": _select(files, CI),
        "agent_rules": _select(files, AGENT_RULES),
        "commit_samples": samples,
        "ticket_keys": keys[:10],
    }


def _summary(res):
    on = lambda d: ", ".join(k for k, v in d.items() if v) or "none"  # noqa: E731
    lines = [
        "host: %s" % res["host"],
        "remote: %s" % (res["remote_url"] or "-"),
        "default base: %s" % (res["default_base"] or "-"),
        "clis: %s" % on(res["clis"]),
        "stack tools: %s" % on(res["stack_tools"]),
    ]
    for label, key in (("policy files", "policy_files"), ("PR templates", "pr_templates"),
                       ("CI files", "ci_files"), ("agent rules", "agent_rules"),
                       ("ticket keys", "ticket_keys")):
        lines.append("%s: %s" % (label, ", ".join(res[key]) or "none"))
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        res = detect_platform(".")
    except (GitError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    text = json.dumps(res, ensure_ascii=False) + "\n" if args.json else _summary(res)
    sys.stdout.buffer.write(text.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
