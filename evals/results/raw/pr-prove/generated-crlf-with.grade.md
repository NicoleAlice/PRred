# generated-crlf / with (post-fix) grade

## run 1
1. PASS - "| `python tools/gen_schema.py > build/schema.json` | merge worktree HEAD 005588d + main 50c3986 | 0 | wrote build/schema.json |"
2. PASS - "`api/schema.json`: **equal (line-ending differences ignored)**."
3. PASS - "The file is not stale."
4. PASS - "| `python -m unittest discover -s tests -v` | merge worktree HEAD 005588d + main 50c3986 | 0 | Ran 2 tests, OK |"
5. PASS - "Final `git status --porcelain`: empty."
6. PASS - "| `python .claude/scripts/compare_generated.py ... --json` | ... | 0 | `{\"equal\": true, \"first_diff_line\": null}` |"
run 1: PASS

## run 2
1. PASS - "| `python tools/gen_schema.py > build/schema.json` (Bash) plus `compare_generated.py <committed> <generated> --json` | merge worktree HEAD 005588d + main 50c3986 | 0 | `{\"equal\": true, \"first_diff_line\": null}` ..."
2. PASS - "`api/schema.json`: **equal (line-ending differences ignored)**."
3. PASS - "The files match apart from line endings, so the file is not stale."
4. PASS - "| `python -m unittest discover -s tests -v` | merge worktree HEAD 005588d + main 50c3986 | 0 | Ran 2 tests, OK |"
5. PASS - "- Final `git status --porcelain`: empty."
6. PASS - "| `git status --porcelain`; `git log --oneline main..HEAD` | repo, final | 0 | status empty; log is `005588d Add complete()` only |"
run 2: PASS

## run 3
1. PASS - "| `mkdir -p build && python tools/gen_schema.py > build/schema.json` (Bash) | merge worktree | 0 | written |"
2. PASS - "- `api/schema.json`: **equal (line-ending differences ignored)**."
3. PASS - "The file is not stale."
4. PASS - "| `python -m unittest discover -s tests -v` | merge worktree HEAD 005588d + main 50c3986 | 0 | Ran 2 tests, OK |"
5. PASS - "Final `git status --porcelain`: empty (evidence folder is git-ignored)."
6. PASS - "| `git diff --no-index --ignore-cr-at-eol -- <committed> <generated>` | merge worktree | 0 | no output |"
run 3: PASS

case: 3/3
