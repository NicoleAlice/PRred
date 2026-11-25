# Cold review prompt

Use this for `pr-cold-review`. The reviewer is a fresh agent with none of the conversation. Give it the worktree, the files to read for context and the rules the change must keep. Do not give it your conclusions or hypotheses: an agent handed a hypothesis tends to confirm it.

Fill the placeholders and send:

```
Cold review, read-only: no edits, no network calls. The change is the diff on
branch <branch> in <path>.
Read for context: <the docs and code the change relies on>.
The rule the change must keep: <e.g. no request writes to the database or
calls an external service>.
Answer with file:line evidence, ranked by severity:
1. Anything that breaks the rule above.
2. Any way a secret or token could reach a log, a test result, a summary or
an exception.
3. Pipeline expressions or steps that do not behave as written.
4. Premises that are untested or wrong.
5. Comments that say something the code does not.
6. Anything a reviewer would refuse.
Say "no finding" for a category you checked and found clean.
```

## After the answer

Check every finding against the code before acting on it. A finding is a claim, not a fact. Mark each one confirmed, refuted (with the file:line that refutes it) or unverified. Fix the confirmed ones, then rerun the tests and the mutations before the PR goes up.

Typical findings a local run misses: a comment that names the wrong pipeline, a safety comment resting on a false premise, a request that logs a noisy warning on every scheduled run, a secret visible to a step that doesn't need it, and a missing setting that leaves a scheduled job green while it tests nothing.
