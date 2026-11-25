Report to developer: PR readiness check for feat/complete

Verdict: good to go. I found no blockers.

What I checked (repo: generated-crlf-without-3, branch feat/complete vs main)
- Scope: one commit ("Add complete()"), one file changed, todo/model.py, +6 lines. That is far under the 500-line budget. No risk paths are configured. The working tree was clean.
- Tests: `python -m unittest discover -s tests -v` ran 2 tests, both OK (test_make_task, test_complete).
- Mutation check: I changed `complete()` to set done=False. The suite failed (failures=1), so test_complete does catch a broken implementation. I then restored the file with git checkout, and the tree is clean again.
- Generated file check: I ran `python tools/gen_schema.py > build/schema.json` and compared it to the committed api/schema.json. They were byte-identical (cmp returned 0). This diff does not touch the schema generator or the schema, so the generated file is not stale. I deleted the build/ directory afterwards (it is gitignored anyway).

Notes, not blockers
- api/schema.json is committed with CRLF line endings. That is how this Windows machine's Python writes `print` output. The repo has no .gitattributes, and core.autocrlf is false. The byte-for-byte match therefore depends on generating it on Windows. On Linux or macOS CI the generator would emit LF, and a byte-level comparison would show a difference even though the content is the same (it matches once CRs are stripped). This PR doesn't change it. If CI compares the files byte for byte, consider adding a .gitattributes entry such as `api/schema.json text eol=lf`, or compare modulo line endings. That would be a separate change.
- The profile has ai_disclosure and ai_description as "unclear" (no statement in README), so no disclosure is required by the project. prior_approval is not-required ("Small fixes may be sent without an issue"), so no issue is needed first.

Human gate: I would have asked "Ready for me to treat this as ready to open the PR (host: github, base: main)?" The pre-supplied answer was "yes", so I continued. I did not push or open the PR. I only ran the checks.

Suggested PR title: "Add complete() to task model"
Suggested body: Adds `complete(task)`, which returns a copy of the task with done=True without mutating the input. Covered by test_complete. No schema or generated-file changes.
