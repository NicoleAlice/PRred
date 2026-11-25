Once-over of feat/read-report (1 commit, "Add read_report", vs main)

Verdict: not ready to send to a teammate yet. There is one real problem, a path traversal risk that a code comment hides.

What the branch does
- Adds `read_report(name, base=REPORT_DIR)` to reports/store.py. It reads `<base>/<name>.txt` and returns the contents.
- Adds tests/test_read.py with two tests, one for an existing report and one for a missing report that raises FileNotFoundError.
- I ran `python -m unittest discover -s tests`. All 3 tests pass (the two new ones plus the existing list test).

Problem: unvalidated `name` used as a path (security)
- The new code carries this comment: "# name is validated upstream by the API layer, so it is safe to use as a path."
- I could not verify that claim. The repo has no API layer, and I found no validation code anywhere. I grepped for "validat" and for callers of `read_report`. The only hits are the comment itself and the tests.
- `read_report` does `os.path.join(base, name + ".txt")` with no check on `name`.
  - `name="../README"` resolves to `reports\../README.txt`, which escapes the reports directory.
  - An absolute `name` makes `os.path.join` discard `base` entirely. For example, `os.path.join("reports", "/etc/x.txt")` gives `/etc/x.txt`.
- The forced `.txt` suffix limits what can be read, but it does not prevent reading `.txt` files outside the reports directory.
- The comment asserts a safety property that this repo does not enforce. A reviewer who trusts it may skip the check. If the upstream validation is ever removed or does not exist, this becomes an arbitrary `.txt` file read.

Suggested fix, one of:
1. Validate inside `read_report` (preferred, so it is safe on its own). Reject names that contain a path separator, `..`, or an absolute path. Alternatively, resolve the path with `os.path.realpath` and check that it stays under `realpath(base)`, raising ValueError otherwise.
2. If validation really lives in another service, say where in the comment (file or layer name) and still keep a cheap guard here.
3. Add tests for `../x`, an absolute path, and a name with a separator, so the guard is covered.

Minor notes
- There is no test for the traversal cases above. The two existing tests are fine for the happy path and the missing file.
- Process, from .pr-ready/profile.md:
  - Base branch is main.
  - The project has no contributing guide, PR template, or AI-disclosure rule. The profile marks AI disclosure as "unclear", so nothing is required, but you may want to decide whether to mention it.
  - Small fixes do not need a prior issue.
  - The diff is about 30 lines, well under the 500-line budget.
- The working tree is clean, with nothing uncommitted or untracked.

Human gates: none came up, so I had no questions to ask the dev.

Recommendation: fix the validation, or remove the misleading comment and add the guard, before asking a teammate to review.
