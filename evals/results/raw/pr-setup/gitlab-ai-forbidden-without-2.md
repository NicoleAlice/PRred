# Report: gitlab-ai-forbidden-without-2

I inspected the repo (.gitlab-ci.yml, CONTRIBUTING.md, MR template, README, requirements.txt, code). I showed the draft profile first, then asked the gate question: "Does this draft look right to save as .pr-ready/profile.md?" The dev answer was "approve", so I saved it to .pr-ready/profile.md in the repo. I changed nothing else.

Key content of the profile:
- Platform: GitLab, so merge requests.
- Run CI locally: `pip install -r requirements.txt` then `pytest -q` (python 3.12). No linters.
- Generated files: none.
- Contribution rules: run `pytest -q` before opening an MR. Small fixes need no issue; larger changes need a discussion first.
- AI rules: AI-written MR descriptions are forbidden, and editor code completion is fine. The assistant must not draft the MR description. It may only list what the template asks for (What changed / Why / How to test).
- Open question: CONTRIBUTING.md is silent on AI-written code beyond completion.
