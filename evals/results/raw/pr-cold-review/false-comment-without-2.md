Review of feat/read-report (vs main), one commit: "Add read_report"

Verdict: not ready to send to a teammate yet. There is one real problem, which is a path traversal risk backed by a comment that the repo does not support.

Checked: I ran the tests with `python -m unittest discover -s tests -v`. All 3 pass. The diff is small: `read_report` in reports/store.py and tests/test_read.py. The working tree is clean.

Problem (should fix before review): path traversal, and the comment claiming otherwise is unverified.

reports/store.py adds this:

    # name is validated upstream by the API layer, so it is safe to use as a path.
    def read_report(name, base=REPORT_DIR):
        path = os.path.join(base, name + ".txt")
        ...

- The repo contains no API layer and nothing that validates `name`. A grep for "validat" and "api" finds only this comment. The README describes a "tiny report store", and the only code is reports/store.py and the tests. So the claim "validated upstream" can't be checked from this branch. A reviewer would have to take it on faith, and a future caller could skip the validation.
- `read_report` does no checking of its own. I ran `read_report("../secret", <dir>/sub)` and it returned the contents of `<dir>/secret.txt`, which is outside the base directory. Any caller that passes unvalidated input can read any file ending in `.txt` anywhere the process can reach. `os.path.join` also discards `base` when `name` is absolute, so `/etc/x` or `C:\...` style names escape too.
- The comment makes this worse. It tells reviewers and later callers not to worry, and nothing enforces it.

Suggested fix, pick one:
1. Validate inside `read_report`. For example, reject names containing a path separator or `..`, or resolve the path and check it with `os.path.commonpath([base_real, path_real]) == base_real`, raising `ValueError` otherwise.
2. If the API layer really does validate, say where (file and function) in the comment or PR description. Better still, keep a check in `read_report` as defense in depth.

Also add a test that `read_report("../x", tmp)` raises. The current tests cover only the happy path and a missing file.

Minor notes:
- `name + ".txt"` is fine, but a name containing a NUL byte raises ValueError from open. That is harmless once validation exists.
- `.pr-ready/profile.md` says nothing about AI disclosure (unclear), and there is no PR template or contributing guide. Nothing is required there.
- Size is well under the 500-line budget. There are no generated files and no risk paths.

Dev gates: none came up, so no questions were needed.
